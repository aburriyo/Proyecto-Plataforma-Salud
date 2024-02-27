import requests

url = "https://api-beta.codegpt.co/api/v1/agent/id"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)