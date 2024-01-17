import asyncio
import pandas as pd
import traceback
from cognite.client import CogniteClient
from authenticate import client as c
from scraper import scraper
from logging_config import configure_logger
from variables import DATABASE_NAME, TABLE_NAME, ID_COLUMN_NAME
from variables import PRICE_MAX_MAX, PRICE_MAX_MIN, PRICE_MIN_MAX, PRICE_MIN_MIN, PRICE_STEP, PRICE_CEILING


logger = configure_logger(__name__)


def initialize_raw(client):
    dbs = client.raw.databases.list(limit=-1).to_pandas()
    if dbs.empty or DATABASE_NAME not in dbs.name.values.tolist():                        
        logger.info(client.raw.databases.create(DATABASE_NAME))
    
    tables = client.raw.tables.list(DATABASE_NAME, limit=-1).to_pandas()
    if tables.empty or TABLE_NAME not in tables.name.values.tolist():
        logger.info(client.raw.tables.create(DATABASE_NAME, TABLE_NAME))


def main(client, nr_of_pages, price_from, price_to):
    
    existing_ids_start = client.raw.rows.list(DATABASE_NAME, TABLE_NAME, limit=-1).to_pandas().index.values.tolist()

    scraped_data = asyncio.run(scraper.main(existing_ids_start, nr_of_pages, price_from, price_to))

    client.raw.rows.insert_dataframe(DATABASE_NAME, TABLE_NAME, pd.DataFrame(scraped_data).fillna('NaN').set_index(ID_COLUMN_NAME))

    existing_ids_end = client.raw.rows.list(DATABASE_NAME, TABLE_NAME, limit=-1).to_pandas().index.values.tolist()

    logger.info(
        f'''\n
        price_from:            {price_from}, \n
        price_to:              {price_to}, \n
        # ad ids at run start: {len(existing_ids_start)}, \n
        # ad ids at run end:   {len(existing_ids_end)}, \n
        # data results:        {len(scraped_data)} \n 
        '''
        )


def handle(client: CogniteClient):

    initialize_raw(client)

    prices_min = [i for i in range(PRICE_MIN_MIN, PRICE_MIN_MAX, PRICE_STEP)]
    prices_max = [i for i in range(PRICE_MAX_MIN, PRICE_MAX_MAX, PRICE_STEP)]
    price_ranges = [(from_, to_) for from_, to_ in zip(prices_min, prices_max)] + [(PRICE_MAX_MAX, PRICE_CEILING)]

    for range_ in price_ranges:
        try:
            main(client, nr_of_pages=51, price_from=range_[0], price_to=range_[1])
       
        except Exception as e:
            logger.error(f"Error on range: {range_}\n Error message:\n {e}")
            traceback.print_exc()



if __name__ == "__main__":
    handle(c)