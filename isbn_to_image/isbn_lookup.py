import requests
from lxml import etree as ET


ISBN_DB_URL = 'https://isbndb.com/book/'


def isbn_lookup(isbn_code):
    '''
    Takes in an isbn code and returns the html result of
    the ISBN DB request for that code
    '''
    request_url = ISBN_DB_URL + str(isbn_code)
    response = requests.get(request_url)
    if response.status_code != 200:
        raise ValueError(
            'Expected 200 code from isbndb, but got %d' % response.status_code
        )
    else:
        return response.content


def isbn_db_html_parse(isbn_db_html):
    '''
    Takes in response html from isbn db and returns
    the link to the isbn db image of the book's cover
    page and a link to the amazon html page if it
    exists
    '''
    parser = ET.HTMLParser(encoding='utf-8')
    html_tree = ET.fromstring(isbn_db_html, parser=parser)
    isbn_image_link = ''
    amazon_link = ''
    # Get the base image stored on isbn db
    for elem in html_tree.iter():
        if elem.tag == 'object':
            attribs = dict(elem.attrib)
            isbn_image_link = attribs['data']
            # Only interested in the first one
            break
    return isbn_image_link, amazon_link
    
    

if __name__ == '__main__':
    response = isbn_lookup(9780735219090)
    isbn_db_html_parse(response)
