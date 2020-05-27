from . import woocommerce

def check_is_in_stock(url, variation_id):
    print('fitnessequipmentireland checking', url, variation_id)
    return woocommerce.check_is_in_stock(url, variation_id)