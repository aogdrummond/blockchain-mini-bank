from flask import Flask
import requests
import os

app = Flask(__name__)



@app.route("/exchange_rate/<from_currency>/<to_currency>",methods=["GET"])
def get_exchange_rate(from_currency,to_currency):
    API_Key = "Sg0r1x6U5LWopRttIkzso9ngAZMTO7aT" #transformar em variável de ambiente
    root_url = "https://api.apilayer.com"
    api_type = "currency_data"
    amount = 1
    endpoint = f"convert?to={from_currency}&from={to_currency}&amount={amount}"
    url = "/".join([root_url,api_type,endpoint]) 
    response = requests.request(method="GET",
                                url=url, 
                                headers={"apikey":API_Key}, 
                                data = {})
    if response.status_code != 200:
        raise Exception("Bad request message")
    
    return response.text

@app.route("/hello-world",methods=["GET"])
def say_hello_world():
    return "Hello World"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)