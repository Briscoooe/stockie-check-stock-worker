from bs4 import BeautifulSoup
import requests
import json

headers = {
    'User-Agent': 'Test User Agent'
}
def check_is_in_stock(url, variation_id):
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')

    product_div = soup.find(action=url)
    products = json.loads(product_div['data-product_variations'])
    is_in_stock = False
    for product in products:
        if product['variation_id'] == variation_id :
            is_in_stock = product['is_in_stock']
    return is_in_stock
    