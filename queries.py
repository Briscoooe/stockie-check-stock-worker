get_products_to_scrape_query = """
    SELECT id, name, url, variant_id, store_id, in_stock
    FROM products
    WHERE active = 1
"""

update_product_in_stock = """
    UPDATE products
    SET in_stock = %s,
    updated_at = NOW()
    WHERE id = %s
"""

update_multiple_products_in_stock = """
    UPDATE products
    SET in_stock = %s,
    updated_at = NOW()
    WHERE id IN (%s)
"""