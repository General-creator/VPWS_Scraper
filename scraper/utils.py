# utils.py
import requests
from bs4 import BeautifulSoup

def get_companies_and_addresses(url):
    company_names = []
    addresses = []

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')

        listings = soup.find_all('div', class_='result')

        for listing in listings:
            company_name_element = listing.find('a', class_='business-name')
            company_name = company_name_element.get_text(strip=True) if company_name_element else "N/A"

            address_element = listing.find('div', class_='street-address')
            address = address_element.get_text(strip=True) if address_element else "N/A"

            city_state_zip_element = listing.find('div', class_='locality')
            city_state_zip = city_state_zip_element.get_text(strip=True) if city_state_zip_element else "N/A"

            full_address = f"{address}, {city_state_zip}"
            
            company_names.append(company_name)
            addresses.append(full_address)

    except requests.RequestException as e:
        print(f"Error requesting page: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return company_names, addresses



