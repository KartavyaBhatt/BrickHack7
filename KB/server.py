import requests

payload={}
headers = {}

barcode = '077890443835'
url = "https://api.wegmans.io/products/barcodes/"+barcode+"?api-version=2018-10-18&subscription-key=d39826cb6b7449279dda03f8b4c70843"
response = requests.request("GET", url, headers=headers, data=payload)
data = response.json()
sku = data['sku']
name = data['name']

print(sku, name)
url = "https://api.wegmans.io/products/" + str(sku) +"?api-version=2018-10-18&subscription-key=d39826cb6b7449279dda03f8b4c70843"
response = requests.request("GET", url, headers=headers, data=payload)
print(response.json().keys())

