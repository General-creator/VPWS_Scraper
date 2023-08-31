import csv
import requests
from bs4 import BeautifulSoup

# Sample function to simulate scraping
def get_companies_and_addresses(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Implement your scraping logic here using BeautifulSoup
        # This is just a placeholder
        company_names = [f'Company {i}' for i in range(1, 11)]
        addresses = [f'Address {i}' for i in range(1, 11)]
        return company_names, addresses
    else:
        response.raise_for_status()

if __name__ == "__main__":
    base_url = 'https://www.yellowpages.com/search'
    search_terms = 'funeral homes'
    location_terms = 'Houston, TX'
    page = 1

    all_company_names = []
    all_addresses = []

    while True:
        url = f'{base_url}?search_terms={search_terms}&geo_location_terms={location_terms}&page={page}'
        try:
            company_names, addresses = get_companies_and_addresses(url)
            if not company_names or not addresses:
                break
            all_company_names.extend(company_names)
            all_addresses.extend(addresses)
            page += 1
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            break

    if len(all_company_names) != len(all_addresses):
        print("Data length mismatch between company names and addresses.")
    else:
        with open('yellowpages_companies.csv', mode='w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file, dialect='excel')
            csv_writer.writerow(['Company Name', 'Address'])

            for company_name, address in zip(all_company_names, all_addresses):
                csv_writer.writerow([company_name, address])

        print("Data exported to yellowpages_companies.csv")


