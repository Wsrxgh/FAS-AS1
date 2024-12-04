from EventManager.Models.RunnerEvents import RunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.RunnerContext import RunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType
from ExtendedTyping.Typing import SupportsStr
from ProgressManager.Output.OutputProcedure import OutputProcedure as output

from typing import Dict, Any, Optional
from pathlib import Path
from os.path import dirname, realpath
import time

from UPISAS.exemplars.wildfire_exemplar import WildFireExemplar
from UPISAS.strategies.adaptive_strategy import WildfireAvoidanceStrategy


class RunnerConfig:
    ROOT_DIR = Path(dirname(realpath(__file__)))

    # ================================ USER SPECIFIC CONFIG ================================
    """The name of the experiment."""
    name: str = "wildfire_experiment"

    """The path to store results from this experiment."""
    results_output_path: Path = ROOT_DIR / 'experiments'

    """Experiment operation type."""
    operation_type: OperationType = OperationType.AUTO

    """The time Experiment Runner will wait after a run completes."""
    time_between_runs_in_ms: int = 1000

    exemplar = None
    strategy = None

    def __init__(self):
        """Executes immediately after program start, on config load."""
        EventSubscriptionController.subscribe_to_multiple_events([
            (RunnerEvents.BEFORE_EXPERIMENT, self.before_experiment),
            (RunnerEvents.BEFORE_RUN, self.before_run),
            (RunnerEvents.START_RUN, self.start_run),
            (RunnerEvents.START_MEASUREMENT, self.start_measurement),
            (RunnerEvents.INTERACT, self.interact),
            (RunnerEvents.STOP_MEASUREMENT, self.stop_measurement),
            (RunnerEvents.STOP_RUN, self.stop_run),
            (RunnerEvents.POPULATE_RUN_DATA, self.populate_run_data),
            (RunnerEvents.AFTER_EXPERIMENT, self.after_experiment)
        ])
        self.run_table_model = None  # Initialized later
        output.console_log("WildFire config loaded")

    def create_run_table_model(self) -> RunTableModel:
        """Create and return the run_table model."""
        self.run_table_model = RunTableModel(
            factors=[],
            exclude_variations=[],
            data_columns=['MR1_total', 'MR2_max']  # Include MR1_total and MR2_max
        )
        return self.run_table_model

    def before_experiment(self) -> None:
        output.console_log("Config.before_experiment() called!")

    def before_run(self) -> None:
        self.exemplar = WildFireExemplar(auto_start=True)
        self.strategy = WildfireAvoidanceStrategy(self.exemplar)
        time.sleep(3)
        output.console_log("Config.before_run() called!")

    def start_run(self, context: RunnerContext) -> None:
        """Configure strategy and prepare for the run."""
        output.console_log("Config.start_run() called!")

    def start_measurement(self, context: RunnerContext) -> None:
        output.console_log("Config.start_measurement() called!")

    def interact(self, context: RunnerContext) -> None:
        """Interact with the WildFireExemplar system."""
        time_slept = 0
        self.strategy.get_monitor_schema()
        self.strategy.get_adaptation_options_schema()
        self.strategy.get_execute_schema()

        while time_slept < 90:
            self.strategy.monitor(verbose=True)
            if self.strategy.analyze():
                if self.strategy.plan():
                    self.strategy.execute()
            time.sleep(3)
            time_slept += 3

        output.console_log("Config.interact() called!")

    def stop_measurement(self, context: RunnerContext) -> None:
        output.console_log("Config.stop_measurement() called!")

    def stop_run(self, context: RunnerContext) -> None:
        output.console_log("Config.stop_run() called! (no container termination)")

    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, SupportsStr]]:
        """
        Process monitored_data and calculate MR1_total and MR2_max.
        """
        output.console_log("Config.populate_run_data() called!")

        monitored_data = self.strategy.knowledge.monitored_data
        MR1_total = 0
        MR2_max = 0

        dynamic_values = monitored_data.get("dynamicValues", [])
        if not isinstance(dynamic_values, list):
            output.console_log("Invalid dynamicValues format!")
            return {"MR1_total": MR1_total, "MR2_max": MR2_max}

        # Process each item in dynamicValues
        for data in dynamic_values:
            if not isinstance(data, dict):
                output.console_log(f"Invalid data format: {data}")
                continue

            MR1 = data.get("MR1", [])
            MR2 = data.get("MR2", 0)

            # Validate and process MR1
            if isinstance(MR1, list) and all(isinstance(x, (int, float)) for x in MR1):
                MR1_total += sum(MR1)
            else:
                output.console_log(f"Invalid MR1 format: {MR1}")

            # Validate and track MR2 maximum
            if isinstance(MR2, (int, float)):
                MR2_max = max(MR2_max, MR2)
            else:
                output.console_log(f"Invalid MR2 format: {MR2}")

        output.console_log(f"Final MR1_total: {MR1_total}, MR2_max: {MR2_max}")
        return {"MR1_total": MR1_total, "MR2_max": MR2_max}

    def after_experiment(self) -> None:
        output.console_log("Config.after_experiment() called!")


    # ================================ DO NOT ALTER BELOW THIS LINE ================================
    experiment_path: Path = None
