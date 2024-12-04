from UPISAS.strategies.adaptive_strategy import WildfireAvoidanceStrategy
#from UPISAS.strategies.wildfire_strategy import WildFireStrategy
from UPISAS.exemplar import Exemplar
from UPISAS.exemplars.wildfire_exemplar import WildFireExemplar  # 假设 WildFireExemplar 类在 wildfire_exemplar.py 文件中
import time
import sys

if __name__ == '__main__':

    wildfire_exemplar = WildFireExemplar(auto_start=True)
    time.sleep(3) 
    #wildfire_exemplar.start_run()
    #time.sleep(3)



    try:

        #strategy = WildFireStrategy(wildfire_exemplar)
        strategy = WildfireAvoidanceStrategy(wildfire_exemplar)
        strategy.get_monitor_schema()
        strategy.get_adaptation_options_schema()
        strategy.get_execute_schema()

        while True:
            input("Try to adapt WildFire?")

            print("\n--- Monitoring WildFire ---")  
            strategy.monitor(verbose=True)

            if strategy.analyze():
                if strategy.plan():
                    strategy.execute()

    except (Exception, KeyboardInterrupt) as e:
        print(str(e))
        print("Stopping WildFire container and exiting...")
        #wildfire_exemplar.stop_container()
        sys.exit(0)
