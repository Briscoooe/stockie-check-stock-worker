from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")

MAX_WORKERS = int(os.getenv("MAX_WORKERS"))

SNS_EU_WEST_ARN_FORMAT="arn:aws:sns:eu-west-1:645069479050:product_id-{}"

SNS_MESSAGE_IN_STOCK_STRING="Product '{}' now in stock! Check here {}"