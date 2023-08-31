import os
import logging
import requests
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template, request, Response
import csv
from io import StringIO

app = Flask(__name__)

# Logging configuration
logging.basicConfig(filename='app.log', level=logging.ERROR)

# Constants (Replace with actual values)
VALID_URL_PREFIXES = ['http://', 'https://']
REQUEST_TIMEOUT = 10
MAX_CONCURRENT_REQUESTS = 5

def is_valid_url(url):
    return url.startswith(VALID_URL_PREFIXES)

def scrape_url(url):
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f"Error requesting {url}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        urls = request.form.getlist('urls')
        valid_urls = [url for url in urls if is_valid_url(url)]
        all_company_names = []
        all_addresses = []

        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_REQUESTS) as executor:
            responses = list(executor.map(scrape_url, valid_urls))

        for response in responses:
            if response:
                # Implement your scraping logic here based on the response
                # This is just a placeholder
                company_names = ['Company A', 'Company B']
                addresses = ['Address 1', 'Address 2']
                all_company_names.extend(company_names)
                all_addresses.extend(addresses)

        return render_template('result.html', company_names=all_company_names, addresses=all_addresses)

    except Exception as e:
        error_message = "An error occurred while scraping. Please try again later."
        logging.error(f"Scraping error: {e}")
        return render_template('error.html', error_message=error_message)

@app.route('/download_csv')
def download_csv():
    csv_data = generate_csv_data()  # Replace with your CSV generation logic
    csv_io = StringIO()

    # Write CSV data to the StringIO object
    csv_writer = csv.writer(csv_io)
    for row in csv_data:
        csv_writer.writerow(row)

    # Create a response with the CSV content
    response = Response(csv_io.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=data.csv'

    return response

def generate_csv_data():
    # Example data (replace this with your scraping logic)
    company_names = ['Company A', 'Company B']
    addresses = ['Address 1', 'Address 2']

    # Combine company names and addresses into rows
    csv_data = [['Company Name', 'Address']]
    for name, address in zip(company_names, addresses):
        csv_data.append([name, address])

    return csv_data

if __name__ == '__main__':
    app.run(debug=True)

