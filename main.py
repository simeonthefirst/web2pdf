import requests
from bs4 import BeautifulSoup
import pdfkit
import os
import re
from urllib.parse import urljoin, urlparse

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)




# Configuration
base_url = 'https://catenax-ev.github.io/docs/next/standards/'  # Replace with the website you want to crawl
start_url = 'overview'  # Replace with subpath where the crawling should start
output_dir = 'output'
pdf_files = []

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to get all links on a page
def get_all_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(url, href)
        if full_url.startswith(base_url):
            links.add(full_url)
    
    return links

# Function to save a page as a PDF
def save_page_as_pdf(url, file_path):
    options = {
        'no-stop-slow-scripts': '',
        'disable-smart-shrinking': '',
        'javascript-delay': '2000',  # Wait time for JavaScript to load
        'no-images': '',  # Option to ignore images (useful if images are missing)
        'disable-javascript': '',  # Option to disable JavaScript (if not required)
        'zoom': '1.3'  # Adjust zoom to ensure the content fits well
    }
    try:
        pdfkit.from_url(url, file_path, configuration=config, options=options)
    except Exception as e:
        print(f"Failed to convert {url} to PDF: {e}")
    pdf_files.append(file_path)


# Crawl the website
def crawl_website(start_url):
    urls_to_visit = {start_url}
    visited_urls = set()
    
    while urls_to_visit:
        current_url = urls_to_visit.pop()
        if current_url in visited_urls:
            continue
        
        visited_urls.add(current_url)
        print(f'Visiting {current_url}')
        
        # Save the page as a PDF
        file_name = re.sub(r'\W+', '_', urlparse(current_url).path) + '.pdf'
        file_path = os.path.join(output_dir, file_name)
        save_page_as_pdf(current_url, file_path)
        
        # Get new links to visit
        new_links = get_all_links(current_url)
        urls_to_visit.update(new_links - visited_urls)

# Start crawling from the base URL
crawl_website(base_url+start_url)

# Merge all PDF files
from PyPDF2 import PdfMerger

merger = PdfMerger()
for pdf in pdf_files:
    merger.append(pdf)
merger.write(os.path.join(output_dir, 'combined.pdf'))
merger.close()

print("PDF created successfully.")
