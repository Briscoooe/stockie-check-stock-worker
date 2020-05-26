from scrapers import *
import sys
import db
import queries
from concurrent import futures
from multiprocessing import Pipe, Process
import concurrent.futures

scraper_map = {
    1: argos,
    2: strengthshop,
    3: irishlifting,
    4: fitnessequipmentireland,
    5: fightstoredublin,
}

def check_row(row):
    in_stock_bool = scraper_map[row["store_id"]].check_is_in_stock(row["url"], row["variant_id"])
    in_stock_tinyint = 1 if in_stock_bool else 0
    return_var = None
    if in_stock_tinyint != row["in_stock"]:
        return_var = (in_stock_tinyint, row["product_id"])
    return return_var

def lambda_handler(event, context):
    print(event)
    try:
        db.connect()
        rows = db.run_select(queries.get_products_to_scrape_query)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(check_row, row): row for row in rows}
            for future in concurrent.futures.as_completed(future_to_url):
                row = future_to_url[future]
                print(row)
                data = future.result()
                print(data)
        # for update in rows_to_update:
            # db.run_update(queries.update_product_in_stock, update)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise