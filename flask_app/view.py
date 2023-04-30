from flask import Flask
from dotenv import load_dotenv
import requests
import os

load_dotenv()
app = Flask(__name__)

@app.route("/exchange_rate/<from_currency>/<to_currency>", methods=["GET"])
def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """
    This function returns the exchange rate between two currencies.

    Args:
        from_currency: The currency to convert from.
        to_currency: The currency to convert to.

    Returns:
        A string representation of the exchange rate.

    Raises:
        Exception: If the API returns a bad request message.
    """
    API_Key = os.environ.get("API_Key")
    root_url = os.environ.get("API_url")
    api_type = os.environ.get("API_type")
    amount = 1
    endpoint = f"convert?to={from_currency}&from={to_currency}&amount={amount}"
    url = "/".join([root_url, api_type, endpoint]) 
    response = requests.request(method="GET", url=url, headers={"apikey":API_Key}, data={})
    if response.status_code != 200:
        raise Exception("Bad request message")
    
    return response.text

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
