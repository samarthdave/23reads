#!/usr/bin/env python3

# domains used for static book image storage
# https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/IMG_SIZE/BOOK_ID.jpg
# https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/IMG_SIZE/BOOK_ID.jpg

# pattern for image size
# .../IMAGE_NUMl --> large
# .../IMAGE_NUMi --> extra large
# add "UX_75..." to the end of the image url to get a 75x100 image

# https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1556036622i/44525305.jpg
# https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1556036622l/44525305.jpg
# https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1556036622i/44525305._UX75_.jpg

import sys
import bs4
import time
import json
from urllib.request import urlopen
from urllib.error import HTTPError


def get_book_id_from_url(book_show_url):

    # if the video id was sent in
    if 'book/show/' not in book_show_url and 'http' not in book_show_url:
        return book_show_url

    booktag_url = None
    try:
        booktag_url = book_show_url.split('book/show/')[1]
    except:
        print('ERROR: Check URL and see if "book/show/" is in it')
        exit(1)

    querystringPosition = booktag_url.find('?')
    if querystringPosition != -1:
        booktag_url = booktag_url[0: querystringPosition]
    return booktag_url


def scrape_book(book_id):
    url = 'https://www.goodreads.com/book/show/' + book_id
    source = urlopen(url)
    soup = bs4.BeautifulSoup(source, 'html.parser')

    # time.sleep(1)

    # find an element in the beautiful soup with class equal to BookCover__Image
    # and get the src attribute
    # cover_url = soup.find('img', {'class': 'BookCover__Image'})['src']

    return {
        'book_id_title':        book_id,
        # 'book_id':              get_id(book_id),
        'book_title':           soup.select_one('h1.Text__title1').text,
        'src':                  soup.select_one('div.BookCover__image img')['src'],
        # "book_series":          get_series_name(soup),
        # "book_series_uri":      get_series_uri(soup),
        # 'top_5_other_editions': get_top_5_other_editions(soup),
        # 'isbn':                 get_isbn(soup),
        # 'isbn13':               get_isbn13(soup),
        # 'year_first_published': get_year_first_published(soup),
        'authorlink':           soup.select_one('a.ContributorLink')['href'],
        'author':               soup.select_one('span.ContributorLink__name').text,
        # 'num_pages':            get_num_pages(soup),
        # 'genres':               get_genres(soup),
        # 'shelves':              get_shelves(soup),
        # 'lists':                get_all_lists(soup),
        # 'num_ratings':          soup.find('meta', {'itemprop': 'ratingCount'})['content'].strip(),
        # 'num_reviews':          soup.find('meta', {'itemprop': 'reviewCount'})['content'].strip(),
        # 'average_rating':       soup.find('span', {'itemprop': 'ratingValue'}).text.strip(),
        # 'rating_distribution':  get_rating_distribution(soup)
    }


def main():
    arguments = sys.argv
    # manually override the youtube URL here or get input manually
    book_url = ''  # 'AcZ2OY5-TeM'
    # print(len(arguments))
    print(arguments)
    if len(arguments) == 2:
        # second argument is book_url
        book_url = arguments[1]

    # or get the input from user and clean it
    if book_url == '':
        book_url = input('Enter book title or URL: ')

    book_url = book_url.strip()
    booktag_name = get_book_id_from_url(book_url)

    try:
        book = scrape_book(booktag_name)
        print('=============================')
        # pretty print the json object "book"
        print(json.dumps(book, indent=4, sort_keys=True))

        print('=============================')
        trimmed = {
            'src': book['src'],
            'alt': book['book_title'],
            'title': book['book_title'],
            'goodreads': book_url
        }
        print(json.dumps(trimmed, indent=4))
        print('=============================')

    except HTTPError as e:
        print(e)
        exit(0)

# END MAIN


if __name__ == '__main__':
    main()

# comment program ends here
# whitespace here is intentional
