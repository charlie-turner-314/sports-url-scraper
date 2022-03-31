
from bs4 import BeautifulSoup


def htmlSoup(html_doc):
    return BeautifulSoup(html_doc, 'html.parser')
