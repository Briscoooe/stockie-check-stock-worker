from . import woocommerce

def check_is_in_stock(url, variant_id):
    print('fitnessequipmentireland checking', url, variant_id)
    return woocommerce.check_is_in_stock(url, variant_id)