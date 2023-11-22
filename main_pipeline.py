from .data import data_management
from .scraper import scraper
from .logging_config.logging_config import configure_logger
import asyncio
import time

logger = configure_logger(__name__)

def main(nr_of_pages):

    mongo_db = data_management.get_database()

    existing_ids0 = data_management.get_existing_ids(mongo_db)

    scraped_data = asyncio.run(scraper.main(existing_ids0, nr_of_pages))
                            
    data_management.insert_data(mongo_db, scraped_data)

    existing_ids1 = data_management.get_existing_ids(mongo_db)

    logger.info(
        f'''\n
        # ids at start: {len(existing_ids0)}, \n
        # ids at end:   {len(existing_ids1)}, \n
        # of results:   {len(scraped_data)} \n 
        '''
        )



if __name__ == "__main__":
    main(nr_of_pages=7)