from bs4 import BeautifulSoup
import requests

not_in_stock_string = 'Currently out of stock'
in_stock_div_id = 'deliveryInformation'

def check_is_in_stock(url, variant_id = None):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    info_text = soup.find(id=in_stock_div_id).get_text()
    return not_in_stock_string not in info_text