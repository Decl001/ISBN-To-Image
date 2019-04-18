import os
import sys
import string
import argparse
import pandas as pd
import numpy as np
from datetime import datetime
from xlrd.biffh import XLRDError

import isbn_lookup 


def load_dataframes(excel_file):
    '''
    Loads the dataframes from the two important sheets in the excel file
    '''
    df_pback = pd.read_excel(excel_file, sheet_name='PB FICTION', header=2)
    df_hback = pd.read_excel(excel_file, sheet_name='HB FICTION', header=2)
    df_pback = df_pback.iloc[:50]
    df_hback = df_hback.iloc[:50]
    df_pback.Isbn = df_pback.Isbn.astype(np.int64)
    df_hback.Isbn = df_hback.Isbn.astype(np.int64)
    return df_pback, df_hback


def setup_folders(output_folder):

    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    else:
        duplication_value = 1
        orig_output_folder = output_folder
        while os.path.isdir(output_folder):
            output_folder = orig_output_folder + '(%d)' % duplication_value
            duplication_value += 1
        os.mkdir(output_folder)
    pb_folder = os.path.join(output_folder, 'Top 50 PB')
    hb_folder = os.path.join(output_folder, 'Top 50 HB')
    os.mkdir(pb_folder)
    os.mkdir(hb_folder)
    return pb_folder, hb_folder


def validate_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join([char for char in filename if char in valid_chars])
    return filename


def dataframe_to_images(df, output_folder):
    created = 0
    errored = []
    for i, (isbn, title) in enumerate(zip(df.Isbn, df.Title)):
        isbn_db_page = isbn_lookup.isbn_lookup(isbn)
        image, _ = isbn_lookup.isbn_db_html_parse(isbn_db_page)
        if image:
            filename = str(i + 1) + '-' + title + '.png'
            filename = validate_filename(filename)
            output_file = os.path.join(output_folder, filename)
            isbn_lookup.get_image(image, output_file)
            created += 1
        else:
            errored.append(title)
    return created, errored

def main(args):
    try:
        df_pback, df_hback = load_dataframes(args.excel_file)
        pb_folder, hb_folder = setup_folders(args.output_folder)
        pb_created, pb_errored = dataframe_to_images(df_pback, pb_folder)
        hb_created, hb_errored = dataframe_to_images(df_hback, hb_folder)
        # print statistics:
        print('Extraction Complete!')
        print('Created %d image files' % (pb_created + hb_created))
        print('Paperback:')
        print('\tCreated: %d' % pb_created)
        print('\tFailed due to no link on the following titles:')
        for title in pb_errored:
            print('\t\t' + title)
        print('\nHardback:')
        print('\tCreated: %d' % hb_created)
        print('\tFailed due to no link on the following titles:')
        for title in hb_errored:
            print('\t\t' + title)
    except FileNotFoundError:
        sys.exit('ERROR: Could not find the excel file specified')
    except XLRDError:
        sys.exit('ERROR: Please specify a valid excel file')



def get_date_str():
    date = datetime.now()
    return date.strftime('%d-%m-%Y')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'excel_file',
        type=str,
        help='The path to the excel file'
    )
    parser.add_argument(
        '--output-folder',
        '-o',
        dest='output_folder',
        type=str,
        help='The folder to store the results in',
        default=get_date_str()
    )
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)