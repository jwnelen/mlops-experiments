import requests
import pandas as pd
import os

from dotenv import load_dotenv
from google.cloud import storage

base_url = "http://api.weatherapi.com/v1/"
current_endpoint = "current.json"

API_KEY, project = None, None

def get_current_weather(q):
	url = f"{base_url}{current_endpoint}?q={q}"
	response = requests.get(url, headers={"key": API_KEY})
	return response.json()

def api_to_gcs(filename):
	q = "Rotterdam"
	data = get_current_weather(q)
	print(data)
	if "error" in data:
		print(data["error"]["message"])
		return
	curr = data["current"]
	del curr["condition"]

	df = pd.DataFrame(curr, index=[0])

	print(df.shape)

	client = storage.Client(project=project)
	bucket = client.get_bucket('example-storage-bucket')

	print(bucket.name)

	blob = bucket.blob(filename)
	blob.upload_from_string(df.to_csv(index=False), "text/csv")
	print("finished uploading")

# Cloud Function
# def main(event, context):
# 	load_dotenv()
# 	global API_KEY
# 	global project
# 	api_to_gcs("weather.csv")

# HTTP
def main(request):
	load_dotenv()
	API_KEY = os.getenv("API_KEY")
	project = os.getenv("PROJECT")
	api_to_gcs("weather.csv")

if __name__ == "__main__":
	main(None)