from data import data_management
from scraper import scraper
from logging_config import configure_logger
import asyncio

logger = configure_logger(__name__)


def main(nr_of_pages):

    mongo_db = data_management.get_database()

    existing_ids_start = data_management.get_existing_ids(mongo_db)

    scraped_data = asyncio.run(scraper.main(existing_ids_start, nr_of_pages))
                            
    data_management.insert_data(mongo_db, scraped_data)

    existing_ids_end = data_management.get_existing_ids(mongo_db)

    logger.info(
        f'''\n
        # ad ids at run start: {len(existing_ids_start)}, \n
        # ad ids at run end:   {len(existing_ids_end)}, \n
        # data results:        {len(scraped_data)} \n 
        '''
        )



if __name__ == "__main__":
    main(nr_of_pages=100)