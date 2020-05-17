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
    out_of_stock = True
    for product in products:
        if product['variation_id'] == variation_id and product['is_in_stock']:
            out_of_stock = False
    return out_of_stock