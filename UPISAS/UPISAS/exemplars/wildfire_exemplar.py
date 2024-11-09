from UPISAS.exemplar import Exemplar
import requests
import logging

class WildFireExemplar(Exemplar):
 
    def __init__(self, auto_start=False):
        self.base_endpoint = "http://localhost:55555"
        if auto_start:
            logging.info("Connected to existing WildFire container.")
    
    def start_run(self):
        pass

    def monitor_fire_status(self):
        url = f"{self.base_endpoint}/monitor"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            logging.info("Fetched fire status successfully.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching fire status: {e}")
            return None

    def execute_fire_control(self, directions):
        url = f"{self.base_endpoint}/execute"
        try:
            response = requests.put(url, json={"uavDetails": directions}, timeout=10)
            response.raise_for_status()
            logging.info("Fire control action executed successfully.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error executing fire control action: {e}")
            return None

    def get_adaptation_options(self):
        url = f"{self.base_endpoint}/adaptation_options"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            logging.info("Fetched adaptation options successfully.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching adaptation options: {e}")
            return None

    def get_monitor_schema(self):
        url = f"{self.base_endpoint}/monitor_schema"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching monitor schema: {e}")
            return None

    def get_execute_schema(self):
        url = f"{self.base_endpoint}/execute_schema"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching execute schema: {e}")
            return None

    def get_adaptation_options_schema(self):
        url = f"{self.base_endpoint}/adaptation_options_schema"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching adaptation options schema: {e}")
            return None
