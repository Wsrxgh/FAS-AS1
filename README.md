### Installation Setup

In the following steps, the installation process for running the project is described.

#### Make

`Make` is required to build and run the Docker image using the provided `Makefile`. While you can manually run the commands without the `Makefile`, using it simplifies the process.

- For Windows users: Download [Make for Windows](https://gnuwin32.sourceforge.net/packages/make.htm).
- For Linux users:
  - Verify installation: Run `make -version`. If a version is displayed, `Make` is already installed.
  - Otherwise, install `Make`:
    ```bash
    sudo apt-get update
    sudo apt-get install make
    ```

#### Docker

Installing Docker is necessary to build and run the Docker image for this project. Refer to the official [Docker documentation](https://docs.docker.com/get-started/get-docker/) for installation instructions tailored to your operating system.

---

### Wildfire Execution

The project runs inside a Docker container. You can interact with it via the REST API or the web interface.

1. Navigate to the `Wildfire-UAVSim-main` folder (where the `Makefile` is located) using a terminal.
2. Execute the following command to start the container:
   ```bash
   make run
   ```
   > **Note:** For the first-time setup, replace `make run` with:
   ```bash
   make runFirst
   ```

To stop the container, press `Ctrl+C` in the terminal. If the container does not terminate, run:
```bash
make stop
```

To remove the container and its image:
```bash
make clean
```

#### Access

- Web Interface: [http://127.0.0.1:8521/](http://127.0.0.1:8521/)
- REST API: [http://127.0.0.1:55555/](http://127.0.0.1:55555/)  
  _Note: The terminal output might display `172.17.0.2:55555` as the API address. This is the container's internal address and can be ignored._

**Next Steps:**  
After starting the container with `make run` or `make runFirst`, access the web interface at [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and click "Start" to begin the experiment.

---

### Running UPISAS and Baseline

#### Prerequisites

- Tested with Python 3.9.12. Compatible with Python 3.8 or higher.

#### Installation

1. Open a terminal and navigate to the `UPISAS` folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Running UPISAS

In the terminal, navigate to the `UPISAS` folder and run:
```bash
python run_.py
```

---

### Running the Experiment Runner

> **Note:**  
> The Experiment Runner does not work on native Windows systems. However, since UPISAS relies on Docker, you should already have the Windows Subsystem for Linux (WSL) installed. Use WSL to run Python for both UPISAS and the Experiment Runner. Restart the UPISAS installation in WSL, then follow these steps:

1. Navigate to the `UPISAS/experiment-runner` folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Return to the parent folder and run:
   ```bash
   sh run_.sh
   ```

---

### Important Notes

- After completing an experiment, delete the folder `experiment_runner_configs/experiments/wildfire_experiment` before starting a new experiment. This ensures proper configuration for the next run.
