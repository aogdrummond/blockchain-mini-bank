import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ExchangeTool:

    def __init__(self):
        self.api_root_url = os.environ.get("API_URL")
        
    def get_rate(self):
        
        from_cur = input("From which currency? ['USD','EUR','JPY' ...] ")
        to_cur = input("To which currency? ['USD','EUR','JPY' ...] ")
        url = self.api_root_url + f"{from_cur}/{to_cur}"
        response = requests.get(url)

        if response.status_code == 200:
            json_response=json.loads(response.text)
            if json_response["success"]:
                quote = json_response["info"]["quote"]
                unix_timestamp = json_response["info"]["timestamp"]
                date = datetime.fromtimestamp(float(unix_timestamp)).date()
                message = f"The exchange rate from {from_cur}" 
                message +=f" to {to_cur} is {quote} on {date}. \n"
                print("Exchange Rate: \n")
                print(message)
                return message
            
            else:
                json_response=json.loads(response.text)
                message = json_response["error"]["info"]
                print(message)
        else:
            print("Failed to obtain the exchange rate information.")

