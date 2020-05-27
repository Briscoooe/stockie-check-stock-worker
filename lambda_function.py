from scrapers import *
import sys
import db
import queries
from concurrent import futures
from multiprocessing import Pipe, Process
import concurrent.futures
import settings

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
        return_var = in_stock_bool
    return return_var

def update_stock_status_for_ids(ids, status):
    if len(ids) > 0:
        sql = queries.update_multiple_products_in_stock
        in_ids = ', '.join(map(lambda x: '%s', ids))
        sql = sql % ('%s', in_ids)
        params = []
        params.append(status)
        params.extend(ids)
        db.run_update(sql, params)

def lambda_handler(event, context):
    print(event)
    try:
        db.connect()
        rows = db.run_select(queries.get_products_to_scrape_query)
        in_stock_true_ids = []; 
        in_stock_false_ids = [];
        with concurrent.futures.ThreadPoolExecutor(max_workers=settings.MAX_WORKERS) as executor:
            future_to_url = {executor.submit(check_row, row): row for row in rows}
            for future in concurrent.futures.as_completed(future_to_url):
                row = future_to_url[future]
                is_in_stock = future.result()
                if is_in_stock is not None:
                    if is_in_stock:
                        in_stock_true_ids.append(row['product_id'])
                    else:
                        in_stock_false_ids.append(row['product_id'])

        update_stock_status_for_ids(in_stock_true_ids, 1)
        update_stock_status_for_ids(in_stock_false_ids, 0)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise