import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ExchangeTool:
    """ExchangeTool class for obtaining exchange rate information."""

    def __init__(self) -> None:
        """
        Initializes ExchangeTool class with API root URL stored in environment variable.
        """
        self.api_root_url = os.environ.get("API_URL")

    def get_rate(self) -> str:
        """
        Returns exchange rate information based on user input.

        Returns:
            str: Exchange rate information message.
        """
        from_cur = input("From which currency? ['USD', 'EUR', 'JPY' ...] ")
        to_cur = input("To which currency? ['USD', 'EUR', 'JPY' ...] ")
        url = f"{self.api_root_url}/{from_cur}/{to_cur}"
        try:
            response = requests.get(url)
        except Exception as e:
            print("")
            print("There is not connection to the API. Did you remember to run Flask container? ")
            print("")
            raise ConnectionError
                
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if json_response["success"]:
                quote = json_response["info"]["quote"]
                unix_timestamp = json_response["info"]["timestamp"]
                date = datetime.fromtimestamp(float(unix_timestamp)).date()
                message = f"The exchange rate from {from_cur}"
                message += f" to {to_cur} is {quote} on {date}. \n"
                print("Exchange Rate: \n")
                print(message)
                return message

            else:
                json_response = json.loads(response.text)
                message = json_response["error"]["info"]
                print(message)
        else:
            print("Failed to obtain the exchange rate information.")
