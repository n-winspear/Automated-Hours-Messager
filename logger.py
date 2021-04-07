import json
from datetime import datetime

class Logger:

    def __init__(self) -> None:
        self.__folder_path = "/home/pi/Documents/Github/Automated-Hours-Messager/logs"
        self.__timestamp = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")

    def create_log(self, response: dict) -> dict:
        filename = f"{self.__timestamp} | {'SUCCESS' if response.status_code == 202 else 'FAILED'}.txt"

        try:
            with open(f"{self.__folder_path}/{filename}", "w") as file:
                file.write(f"Messages sent at {self.__timestamp}\n\n{json.dumps(response.json(), indent=4, sort_keys=True)}")
        except:
            print('Failed to log.', response.json())

    


        