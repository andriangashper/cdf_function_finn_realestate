import aiohttp
import asyncio
from .parse_html import parse_search_page, parse_ad_page
from .variables import search_url, AD_URL_BASE, HEADERS, SEMAPHORE_PARAMETER, FETCH_URL_TIMEOUT, MAX_RETRIES



async def fetch_html(session, url, retries=MAX_RETRIES):
    semaphore = asyncio.Semaphore(SEMAPHORE_PARAMETER) 
    async with semaphore:
        for attempt in range(retries):
            try:
                async with session.get(url, headers=HEADERS, timeout=FETCH_URL_TIMEOUT) as response:
                    return await response.text()
            except asyncio.TimeoutError:
                print(f"Timeout occurred for URL: {url}. \nRetrying attempt {attempt + 1}...")
            except aiohttp.client_exceptions.ServerDisconnectedError:
                print(f"Server disconnected when accessing URL: {url}. \nRetrying attempt {attempt + 1}...")
            except Exception as e:
                print(f"Other error when accessing URL: {url}. \nError: \n{e} \nRetrying attempt {attempt + 1}...")
        
        print(f"Max retries reached for URL: {url}. Skipping.")
        return None


async def process_url(session, url, parse_function):
    print(f"Processing data from URL: {url}")
    html_text = await fetch_html(session, url)
    
    if html_text is not None:
        try:
            result = await parse_function(html_text)
            print(f"Processing completed for URL: {url}")
            return result
        except Exception as e:
            print(f"Error parsing HTML for URL: {url}, \nError: \n{e}")
    else:
        print(f"HTML fetch failed for URL: {url}. Skipping.")
    
    return None


async def main(existing_ad_ids, max_nr_of_search_pages, price_from, price_to):

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:

        search_tasks = [
            asyncio.ensure_future(process_url(session, search_url(page_nr, price_from, price_to), parse_search_page))
            for page_nr in range(1, max_nr_of_search_pages+1)
            ]

        ad_id_lists = await asyncio.gather(*search_tasks)
        ad_ids = []
        for ad_id_list in ad_id_lists:
            for ad_id in ad_id_list:
                if ad_id not in ad_ids:
                    ad_ids.append(ad_id)


        print(f"Obtained {len(ad_ids)} ad ids.")
        print(f"# existing ad ids: {len(existing_ad_ids)}")

        new_ad_ids = [ad_id for ad_id in ad_ids if ad_id not in existing_ad_ids]
        print(f"# new ad ids: {len(new_ad_ids)}")
        ad_tasks = [
            asyncio.ensure_future(process_url(session, AD_URL_BASE+ad_id, parse_ad_page))
            for ad_id in new_ad_ids
            ]  

        ad_data = await asyncio.gather(*ad_tasks)
        ad_data = [result | {"ad_id":ad_id} for ad_id, result in zip(new_ad_ids, ad_data) if result]

        print(f"# result rows: {len(ad_data)}")

    return ad_data



if __name__ == "__main__":
    print("Running local test!")

    results = asyncio.run(main([],1))
    
    print(f"Test data: \n{results[0]}")