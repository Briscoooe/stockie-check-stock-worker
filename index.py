from scrapers import *

in_stock = argos.check_is_in_stock('https://www.argos.ie/static/Product/partNumber/6187783/Trail/searchtext%3EKETTLEBELL.htm')
print(in_stock)