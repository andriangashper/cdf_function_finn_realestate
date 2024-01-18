SEARCH_URL_BASE = "https://www.finn.no/realestate/homes/search.html?"
AD_URL_BASE = "https://www.finn.no/realestate/homes/ad.html?finnkode="
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
SEMAPHORE_PARAMETER = 3
FETCH_URL_TIMEOUT = 10
MAX_RETRIES = 5

def search_url(page, price_from, price_to):
    return SEARCH_URL_BASE+f"page={page}&price_from={price_from}&price_to={price_to}"