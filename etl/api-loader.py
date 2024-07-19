import requests
import os
import pandas as pd

from dotenv import load_dotenv
from google.cloud import storage

base_url = "http://api.weatherapi.com/v1/"
current_endpoint = "current.json"

if __name__ == "__main__":
	load_dotenv(".env") 
	API_KEY = os.getenv("API_KEY")
	project = os.getenv("PROJECT_ID")

def api_to_gcs(filename):
	def get_current_weather(q):
		url = f"{base_url}{current_endpoint}?q={q}"
		response = requests.get(url, headers={"key": API_KEY})
		return response.json()

	q = "Rotterdam"
	data = get_current_weather(q)
	curr = data["current"]
	del curr["condition"]

	df = pd.DataFrame(curr, index=[0])

	client = storage.Client(project=project)
	bucket = client.get_bucket('example-storage-bucket')

	blob = bucket.blob(filename)
	blob.upload_from_string(df.to_csv(index=False), "text/csv")