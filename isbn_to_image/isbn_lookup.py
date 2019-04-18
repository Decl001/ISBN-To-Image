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
    # Find the table of sites
    table_class = 'table table-hover'
    #ßprint(type(table_class))
    table_elem = None
    for elem in html_tree.iter():
        if elem.tag == 'table':
            attribs = dict(elem.attrib)
            if 'class' in attribs:
                if attribs['class'] == table_class:
                    table_elem = elem
                    break
    
    for sub_elem in table_elem:
        if sub_elem.tag == 'tr' and b'amazon' in ET.tostring(sub_elem):
            for td_elem in sub_elem:
                if len(td_elem):  # pylint: disable=C1801
                    for child in td_elem:
                        if child.tag == 'a':
                            attribs = dict(child.attrib)
                            amazon_link = attribs['href']
                            break
            break

    return isbn_image_link, amazon_link
    

def get_image(image_link, output_filename):
    response = requests.get(image_link)
    if response.status_code == 200:
        with open(output_filename, 'wb') as img_file:
            img_file.write(response.content)
    else:
        raise ValueError(
            'Expected 200 response code but got: %d' % response.status_code
        )

if __name__ == '__main__':
    with open('../isb.html', 'rb') as f:
        response = f.read()
    isbn_link, amazon_link = isbn_db_html_parse(response)
