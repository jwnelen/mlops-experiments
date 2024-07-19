import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd

base_url = "http://api.weatherapi.com/v1/"
current_endpoint = "current.json"

load_dotenv(".env") 

KEY = os.getenv("API_KEY")

def get_current_weather(q):
    url = f"{base_url}{current_endpoint}?q={q}"
    response = requests.get(url, headers={"key": KEY})
    return response.json()

q = "Rotterdam"
data = get_current_weather(q)
curr = data["current"]
del curr["condition"]

df = pd.DataFrame(curr, index=[0])

print(df)