from bs4 import BeautifulSoup
import requests

not_in_stock_string = 'Out of stock'
stock_available_class = 'availability out-of-stock'

def check_is_in_stock(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    info_text = soup.find('p', { 'class': stock_available_class}).get_text()
    return not_in_stock_string in info_text