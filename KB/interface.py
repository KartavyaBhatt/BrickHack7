import requests

class API:
    def addItem(self, barcode):
        payload={}
        headers = {}

        # barcode = '077890443835'
        url = "https://api.wegmans.io/products/barcodes/"+barcode+"?api-version=2018-10-18&subscription-key=d39826cb6b7449279dda03f8b4c70843"
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        sku = data['sku']
        name = data['name']

        url = "https://api.wegmans.io/products/" + str(sku) +"?api-version=2018-10-18&subscription-key=d39826cb6b7449279dda03f8b4c70843"
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        for item in data["nutrients"]:
            if item["type"] == "Calories":
                calories = item['quantity']
                break

        for item in data["tradeIdentifiers"]:
            if item["images"] is not None:
                img = item['images'][0]
                break

        url = "https://api.wegmans.io/products/"+ str(sku) +"/prices/25?api-version=2018-10-18&subscription-key=d39826cb6b7449279dda03f8b4c70843"
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        price = data["price"]
        quantity = 1

        data = {'_id': sku,
        'pName': name,
        'pCal': calories,
        'pPrice': price,
        'pQuantity': quantity,
        'pImage': img}
        
        return data