import os
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BASE_URL = os.getenv("BASE_URL")
CLIENT_NAME = os.getenv("CLIENT_NAME")
PROJECT_NAME = os.getenv("PROJECT_NAME")

DATABASE_NAME = "raw_001_finn_realestate"
TABLE_NAME = "finn_realestate_scraped_data"
ID_COLUMN_NAME = "ad_id"

FUNCTION_NAME = "scrape_finn_realestate_data"
FUNCTION_EXTERNAL_ID = "fn_001_scrape_finn_realestate_data"

PRICE_MIN_MIN = 0
PRICE_MIN_MAX = 20000000
PRICE_MAX_MIN = 499999
PRICE_MAX_MAX = 24999999
PRICE_STEP = 500000
PRICE_CEILING = 100000000