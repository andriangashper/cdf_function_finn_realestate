from bs4 import BeautifulSoup
from logging_config import configure_logger

logger = configure_logger(__name__)


async def parse_search_page(html_text):
    try:
        soup = BeautifulSoup(html_text, "html.parser")
        divs = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['absolute'])
        return [div["aria-owns"].split("-")[-1] for div in divs]
    
    except Exception as e:
        logger.error(f"Prasing failed for Search page, Error: {str(e)[:1000]}")


async def parse_ad_page(html_text):
    try:
        soup = BeautifulSoup(html_text, "html.parser")
        
        title_tag = soup.find("h1")
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else None

        location_tag = soup.find("span", {"data-testid": "object-address"})
        location = location_tag.get_text(strip=True) if location_tag else None

        price_tag = soup.find("div", {"data-testid": "pricing-incicative-price"})
        price = int(price_tag.find("span", {"class": "text-28 font-bold"}).get_text(strip=True)\
            .replace(" kr", "").replace("\xa0", "").replace(",", ".")) if price_tag else None

        property_type_tag = soup.find("div", {"data-testid": "info-property-type"})
        property_type = property_type_tag.dd.get_text(strip=True) if property_type_tag else None

        nr_of_bedrooms_tag = soup.find("div", {"data-testid": "info-bedrooms"})
        nr_of_bedrooms = int(nr_of_bedrooms_tag.dd.get_text(strip=True)) if nr_of_bedrooms_tag else None

        nr_of_rooms_tag = soup.find("div", {"data-testid": "info-rooms"})
        nr_of_rooms = int(nr_of_rooms_tag.dd.get_text(strip=True)) if nr_of_rooms_tag else None

        primary_area_tag = soup.find("div", {"data-testid": "info-primary-area"})
        primary_area = int(primary_area_tag.dd.get_text(strip=True).replace("\xa0", "").replace(" m²", "")) if primary_area_tag else None

        usable_area_tag = soup.find("div", {"data-testid": "info-usable-area"})
        usable_area = int(usable_area_tag.dd.get_text(strip=True).replace("\xa0", "").replace(" m²", "")) if usable_area_tag else None

        plot_area_tag = soup.find("div", {"data-testid": "info-plot-area"})
        plot_area = int(plot_area_tag.dd.get_text(strip=True).replace("\xa0", "").replace(" m² (eiet)", "")) if plot_area_tag else None

        floot_tag = soup.find("div", {"data-testid": "info-floor"})
        floor_ = int(floot_tag.dd.get_text(strip=True)) if floot_tag else None

        construction_year_tag = soup.find("div", {"data-testid": "info-construction-year"})
        construction_year = int(construction_year_tag.dd.get_text(strip=True)) if construction_year_tag else None

        renovated_year_tag = soup.find("div", {"data-testid": "info-renovated-year"})
        renovated_year = int(renovated_year_tag.dd.get_text(strip=True)) if renovated_year_tag else None

        energy_label_tag = soup.find("span", {"data-testid": "energy-label-info"})
        energy_label = energy_label_tag.get_text(strip=True) if energy_label_tag else None

        facilities = soup.find_all("div", {"class" : "py-4 break-words"})
        facilities = [i.get_text(strip=True) for i in facilities] if facilities else None

        about_home = soup.find_all("div", {"class" : "description-area whitespace-pre-wrap"})
        about_home = " ".join([i.get_text(strip=True) for i in about_home]) if about_home else None

        return {"title":title,
                "location":location,
                "price":price,
                "property_type":property_type,
                "nr_of_bedrooms":nr_of_bedrooms,
                "nr_of_rooms":nr_of_rooms,
                "primary_area":primary_area,
                "usable_area":usable_area,
                "plot_area":plot_area,
                "floor":floor_,
                "contruction_year":construction_year,
                "renovated_year":renovated_year,
                "energy_label":energy_label,
                "facilities":facilities,
                "about_home":about_home
                }
    
    except Exception as e:
        logger.error(f"Prasing failed for Ad page, Error: {str(e)[:1000]}")