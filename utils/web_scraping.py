import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from urllib.parse import urljoin, urlparse
import json
import os
from tqdm import tqdm
# User-inputted variables
base_url = "https://www.praxisframework.org/en/"  # Base URL of the website to extract child pages
output_directory = "docs/Praxis_test/"  # Output directory for PDF files
string_to_remove = "/en/"  # Specify the string to remove

# Function to extract text from a specific HTML element by ID
def extract_text_from_html_element(soup, element_id):
    element = soup.find('div', id=element_id)  # Change 'div' to the relevant HTML tag
    if element:
        return element.get_text()
    else:
        return ""

# Function to extract the title from <h1> tags
def extract_title_from_html(soup):
    title_element = soup.find('h1')
    if title_element:
        return title_element.get_text()
    else:
        return ""

# Function to generate a PDF from the extracted text and title
def create_pdf_from_text_and_title(title, text, output_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.multi_cell(0, 10, txt=text.encode('latin-1', 'replace').decode('latin-1'))
    pdf.output(output_file)

# Function to extract all child page URLs from a base URL, recursively
def extract_all_child_page_urls(base_url, visited_pages=None):
    if visited_pages is None:
        visited_pages = set()

    if base_url in visited_pages:
        return set()

    response = requests.get(base_url)
    if response.status_code == 200:
        visited_pages.add(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract child page URLs that start with the base URL
        child_page_urls = set()
        for link in soup.find_all('a', href=True):
            child_url = urljoin(base_url, link['href'])
            if child_url.startswith(base_url):
                child_page_urls.update(extract_all_child_page_urls(child_url, visited_pages))

        child_page_urls.add(base_url)  # Add the current URL to the set

        return child_page_urls
    else:
        print(f"Failed to fetch the base webpage: {base_url}. Status code: {response.status_code}")
        return set()

if __name__ == "__main__":
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Extract all child page URLs
    child_page_urls = extract_all_child_page_urls(base_url)

    # Create a dictionary to store the relative file path of PDFs mapped to full URLs
    pdf_url_mapping = {}

    if child_page_urls:
        for child_url in tqdm(child_page_urls):
            response = requests.get(child_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract title from <h1> tag
                title = extract_title_from_html(soup)

                # Extract text from the 'content' element
                extracted_text = extract_text_from_html_element(soup, "content")

                if extracted_text:
                    # Get the page name from the URL and sanitize it for the file name
                    page_name = urlparse(child_url).path

                    # Remove the specified string from the filename
                    if string_to_remove in page_name:
                        page_name = page_name.replace(string_to_remove, '')

                    # Replace '/' with '_' in the filename
                    page_name = page_name.replace('/', '_')

                    output_file = os.path.join(output_directory, page_name + ".pdf")
                    create_pdf_from_text_and_title(title, extracted_text, output_file)
                    print(f"PDF file '{output_file}' created successfully.")

                    # Store the relative file path of the PDF mapped to the full URL
                    pdf_url_mapping[output_file] = child_url
            else:
                print(f"Failed to fetch child page: {child_url}. Status code: {response.status_code}")

    # Create a JSON file to store the relative file path of PDFs mapped to full URLs
    json_filename = "pdf_url_mapping.json"
    with open(json_filename, 'w') as json_file:
        json.dump(pdf_url_mapping, json_file, indent=4)

    print(f"PDF-URL mapping JSON file '{json_filename}' created successfully.")