import aiohttp
import asyncio
from parse_html import parse_search_page, parse_ad_page
from logging_config import configure_logger

logger = configure_logger(__name__)

existing_ad_ids = []

SEARCH_URL_BASE = "https://www.finn.no/realestate/homes/search.html?page="
AD_URL_BASE = "https://www.finn.no/realestate/homes/ad.html?finnkode="
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
MAX_NR_OF_SEARCH_PAGES = 1

semaphore = asyncio.Semaphore(100)

async def fetch_html(session, url):
    async with semaphore:
        async with session.get(url, headers=HEADERS) as response:
            return await response.text()
    

async def process_url(session, url, parse_function):
    logger.info((f"Processing data from URL: {url}"))
    try:
        html_text = await fetch_html(session, url)
        return await parse_function(html_text)

    except aiohttp.ClientError as e:
        logger.error(f"Request failed for URL: {url}, Error: {e}")
        return None


async def main(existing_ad_ids):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        search_tasks = [process_url(session, SEARCH_URL_BASE+str(page_nr+1), parse_search_page) 
                        for page_nr in range(MAX_NR_OF_SEARCH_PAGES)]

        ad_id_lists = await asyncio.gather(*search_tasks)

        ad_ids = [ad_id for ad_id_list in ad_id_lists for ad_id in ad_id_list]

        ad_tasks = [process_url(session, AD_URL_BASE+ad_id, parse_ad_page) 
                    for ad_id in ad_ids[:20] if ad_id not in existing_ad_ids]  

        ad_data = await asyncio.gather(*ad_tasks)

    return ad_data



if __name__ == "__main__":
    results = asyncio.run(main(existing_ad_ids))
    
    for result in results:
        with open("results.txt", "a+") as t:
            t.write(str(result)+" \n")