import asyncio
import pandas as pd
import time
from cognite.client import CogniteClient
from authenticate import client as c
from scraper import scraper
from variables import DATABASE_NAME, TABLE_NAME, ID_COLUMN_NAME
from variables import PRICE_MAX_MAX, PRICE_MAX_MIN, PRICE_MIN_MAX, PRICE_MIN_MIN, PRICE_STEP, PRICE_CEILING, TIMEOUT_TIME, MAX_NR_OF_PAGES
import random


def initialize_raw(client):
    dbs = client.raw.databases.list(limit=-1).to_pandas()
    if dbs.empty or DATABASE_NAME not in dbs.name.values.tolist():                        
        print(client.raw.databases.create(DATABASE_NAME))
    
    tables = client.raw.tables.list(DATABASE_NAME, limit=-1).to_pandas()
    if tables.empty or TABLE_NAME not in tables.name.values.tolist():
        print(client.raw.tables.create(DATABASE_NAME, TABLE_NAME))


def main(client, nr_of_pages, price_from, price_to):
    
    existing_ids_start = client.raw.rows.list(DATABASE_NAME, TABLE_NAME, limit=-1).to_pandas().index.values.tolist()

    scraped_data = asyncio.run(scraper.main(existing_ids_start, nr_of_pages, price_from, price_to))

    if scraped_data:
        df = pd.DataFrame(scraped_data).fillna('NaN')
        if ID_COLUMN_NAME in df.columns:
            df = df.set_index(ID_COLUMN_NAME)
            client.raw.rows.insert_dataframe(DATABASE_NAME, TABLE_NAME, df)
        else:
            print(f"Column '{ID_COLUMN_NAME}' not found in scraped data.")
    else:
        print("No data scraped.")

    existing_ids_end = client.raw.rows.list(DATABASE_NAME, TABLE_NAME, limit=-1).to_pandas().index.values.tolist()

    print(
        f'''\n
        price_from:            {price_from}, \n
        price_to:              {price_to}, \n
        # ad ids at run start: {len(existing_ids_start)}, \n
        # ad ids at run end:   {len(existing_ids_end)}, \n
        # data results:        {len(scraped_data)} \n 
        '''
        )
    
    return len(scraped_data)


def handle(client: CogniteClient):
    start_time = time.time()

    initialize_raw(client)

    prices_min = [i for i in range(PRICE_MIN_MIN, PRICE_MIN_MAX, PRICE_STEP)]
    prices_max = [i for i in range(PRICE_MAX_MIN, PRICE_MAX_MAX, PRICE_STEP)]
    price_ranges = [(from_, to_) for from_, to_ in zip(prices_min, prices_max)] + [(PRICE_MAX_MAX, PRICE_CEILING)]
    random.shuffle(price_ranges)

    len_scraped_data = 0
    for range_ in price_ranges:
        if time.time() - start_time > TIMEOUT_TIME:
            print(f"Timeout time reached. Scraped {len_scraped_data} rows.")
            break   
        
        len_scraped_data += main(client, nr_of_pages=MAX_NR_OF_PAGES, price_from=range_[0], price_to=range_[1])

    return len_scraped_data



if __name__ == "__main__":
    handle(c)