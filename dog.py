import requests

url = "https://dog.ceo/dog-api/documentation/"

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))