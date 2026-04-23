from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup

def normalize_url(input_url):
    url = urlsplit(input_url)
    return url.netloc + url.path

def get_heading_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    header = soup.find('h1')
    if header is None:
        header = soup.find('h2')
        if header is None:
            return ""
    return header.get_text()

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.main
    if soup.main:
        soup = temp
    if soup.p is None:
        return ""
    return soup.p.get_text()

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    all_elements = soup.find_all('a')
    all_links = []

    if all_elements:
        for elem in all_elements:
            link = elem.get('href')
            if link is None:
                continue
            all_links.append(urljoin(base_url, link))

    return all_links

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')

    all_elements = soup.find_all('img')
    all_links = []

    if all_elements:
        for elem in all_elements:
            link = elem.get('src')
            if link is None:
                continue
            all_links.append(urljoin(base_url, link))

    return all_links

def extract_page_data(html, page_url):
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url)
    }
