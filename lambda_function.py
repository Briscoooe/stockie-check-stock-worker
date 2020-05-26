from scrapers import *
import sys
import db
import queries
from concurrent import futures
from multiprocessing import Pool, Queue, Process

scraper_map = {
    1: argos,
    2: strengthshop,
    3: irishlifting,
    4: fitnessequipmentireland,
    5: fightstoredublin,
}

def check_row(queue, row):
    in_stock_bool = scraper_map[row["store_id"]].check_is_in_stock(row["url"], row["variant_id"])
    in_stock_tinyint = 1 if in_stock_bool else 0
    if in_stock_tinyint != row["in_stock"]:
        queue.put((in_stock_tinyint, row["product_id"]))
    else:
        queue.put(None)

def lambda_handler(event, context):
    print(event)
    try:
        db.connect()
        rows = db.run_select(queries.get_products_to_scrape_query)
        q = Queue()
        processes = []
        rows_to_update = []
        for row in rows:
            p = Process(target=check_row, args=(q, row))
            processes.append(p)
            p.start()
            print('started')
        for p in processes:
            update = q.get()
            if update is not None:
                rows_to_update.append(update)
            print('processed')
        for p in processes:
            p.join()
            print('joined')
        for update in rows_to_update:
            db.run_update(queries.update_product_in_stock, update)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
