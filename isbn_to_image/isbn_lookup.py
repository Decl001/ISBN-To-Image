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


if __name__ == '__main__':
    response = isbn_lookup(9780735219090)
    print(response)
