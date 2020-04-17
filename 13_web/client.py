import requests

url = 'https://127.0.0.1:5000/'

res = requests.get(url, verify=False)

print(res.text)