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

def reader_proc(pipe):
    ## Read from the pipe; this will be spawned as a separate Process
    p_output, p_input = pipe
    p_input.close()    # We are only reading
    while True:
        msg = p_output.recv()    # Read from the output pipe and do nothing
        print(msg)
        if msg=='DONE':
            break

def lambda_handler(event, context):
    print(event)
    try:
        db.connect()
        rows = db.run_select(queries.get_products_to_scrape_query)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(check_row, row): row for row in rows}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                data = future.result()
                print(data)
        # for update in rows_to_update:
            # db.run_update(queries.update_product_in_stock, update)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
lambda_handler(None, None)