get_products_to_scrape_query = """
    SELECT product_id, url, variant_id, store_id, in_stock
    FROM products
    WHERE active = 1
    AND deleted_at IS NULL
"""

update_product_in_stock = """
    UPDATE products
    SET in_stock = %s,
    updated_at = NOW()
    WHERE product_id = %s
"""
