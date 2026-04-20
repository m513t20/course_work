import requests

from Config import *

class NetworkManager:
    def get_start_state(self, reset):
        try:
            requests.post("http://127.0.0.1:8000/register", json = {"name" : STORAGE_NAME, "source_url": CV_URL}, timeout=5)
            if reset:
                requests.post(f"{BASE_URL}/reset", timeout=5)
            response = requests.get(f"{BASE_URL}/data", timeout=5)
            return response.json()            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка сети (GET): {e}")
            return None

    def get_board_state(self):
        try:
            response = requests.get(f"{BASE_URL}/step", timeout=5)
            return response.json()            
        except requests.exceptions.RequestException as e:
            print(f"Ошибка сети (GET): {e}")
            return None
     