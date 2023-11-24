from data import data_management
from scraper import scraper
from logging_config import configure_logger
import asyncio
import time

logger = configure_logger(__name__)


def main(nr_of_pages, price_from, price_to):

    loop = asyncio.get_event_loop()

    mongo_db = data_management.get_database()

    existing_ids_start = data_management.get_existing_ids(mongo_db)

    scraped_data = loop.run_until_complete(scraper.main(existing_ids_start, nr_of_pages, price_from, price_to))
                            
    data_management.insert_data(mongo_db, scraped_data)

    existing_ids_end = data_management.get_existing_ids(mongo_db)

    logger.info(
        f'''\n
        price_from:            {price_from}, \n
        price_to:              {price_to}, \n
        # ad ids at run start: {len(existing_ids_start)}, \n
        # ad ids at run end:   {len(existing_ids_end)}, \n
        # data results:        {len(scraped_data)} \n 
        '''
        )



if __name__ == "__main__":
    prices_min = [i for i in range(0, 20000000, 500000)]
    prices_max = [i for i in range(499999, 24999999, 500000)]
    price_ranges = [(from_, to_) for from_, to_ in zip(prices_min, prices_max)] + [(20000000,100000000)]

    for range in price_ranges:
        try:
            main(nr_of_pages=51, price_from=range[0], price_to=range[1])
        except Exception as e:
            logger.error(f"Error on range: {range}\n Error message:\n {e}")