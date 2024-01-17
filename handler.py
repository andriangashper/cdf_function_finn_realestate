import asyncio
import pandas as pd
import traceback
from scraper import scraper
from logging_config import configure_logger
from authenticate import client
from variables import DATABASE_NAME, TABLE_NAME, ID_COLUMN_NAME
from variables import PRICE_MAX_MAX, PRICE_MAX_MIN, PRICE_MIN_MAX, PRICE_MIN_MIN, PRICE_STEP, PRICE_CEILING


logger = configure_logger(__name__)


def initialize_raw():
    if DATABASE_NAME not in client.raw.databases.list(limit=-1).to_pandas().name.values.tolist():                        
        logger.info(client.raw.databases.create(DATABASE_NAME))
    
    if TABLE_NAME not in client.raw.tables.list(DATABASE_NAME, limit=-1).to_pandas().name.values.tolist():
        logger.info(client.raw.tables.create(DATABASE_NAME, TABLE_NAME))


def get_existing_ids():
    columns = client.raw.rows.list(DATABASE_NAME, TABLE_NAME).to_pandas().columns
    if ID_COLUMN_NAME in columns:
        return client.raw.rows.list(DATABASE_NAME, TABLE_NAME, columns=[ID_COLUMN_NAME], limit=-1).to_pandas()[ID_COLUMN_NAME].values.tolist()
    else:
        return []


def main(nr_of_pages, price_from, price_to):
    
    existing_ids_start = get_existing_ids()

    loop = asyncio.get_event_loop()
    scraped_data = loop.run_until_complete(scraper.main(existing_ids_start, nr_of_pages, price_from, price_to))
    
    client.raw.rows.insert_dataframe(DATABASE_NAME, TABLE_NAME, pd.DataFrame(scraped_data).fillna('NaN').set_index(ID_COLUMN_NAME))

    existing_ids_end = get_existing_ids()

    logger.info(
        f'''\n
        price_from:            {price_from}, \n
        price_to:              {price_to}, \n
        # ad ids at run start: {len(existing_ids_start)}, \n
        # ad ids at run end:   {len(existing_ids_end)}, \n
        # data results:        {len(scraped_data)} \n 
        '''
        )


def handle():

    initialize_raw()

    prices_min = [i for i in range(PRICE_MIN_MIN, PRICE_MIN_MAX, PRICE_STEP)]
    prices_max = [i for i in range(PRICE_MAX_MIN, PRICE_MAX_MAX, PRICE_STEP)]
    price_ranges = [(from_, to_) for from_, to_ in zip(prices_min, prices_max)] + [(PRICE_MAX_MAX, PRICE_CEILING)]

    for range in price_ranges:
        try:
            main(nr_of_pages=51, price_from=range[0], price_to=range[1])
       
        except Exception as e:
            logger.error(f"Error on range: {range}\n Error message:\n {e}")
            traceback.print_exc()



# if __name__ == "__main__":
#     handle()