import woocommerce

def check_is_in_stock(url, variation_id):
    return woocommerce.check_is_in_stock(url, variation_id)