from urllib.parse import urlsplit
from bs4 import BeautifulSoup

def normalize_url(input_url):
    url = urlsplit(input_url)
    return url.netloc + url.path

def get_heading_from_html(html):

