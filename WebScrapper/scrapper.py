import requests
import csv
from bs4 import BeautifulSoup

def scrape_page(soup, quotes) :
    quote_elements = soup.find_all('div', class_='quote')

    page_name = soup.find('h1').text

    for quote_element in quote_elements:
        # extract the text of the quote
        text = quote_element.find('span', class_='text').text
        # extract the author of the quote
        author = quote_element.find('small', class_='author').text

        # extract the tag <a> HTML elements related to the quote
        tag_elements = quote_element.find('div', class_='tags').find_all('a', class_='tag')

        # store the list of tag strings in a list
        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)

        quotes.append(
            {
                'nameOfPage' : page_name,
                'text': text,
                'author': author,
                'tags': ', '.join(tags)
            }
        )

base_url = 'https://quotes.toscrape.com'

headers = {
    'User_Agent' : 'Mozilla/5.0 (Linux; Android 10; K) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/134.0.0.0 Mobile Safari/537.36'
}

page = requests.get(base_url, headers = headers)

soup = BeautifulSoup(page.text, 'html.parser')

quotes = []

scrape_page(soup, quotes)

# get the "Next" HTML element
next_li_element = soup.find('li', class_='next')

# if there is a next page to scrape
while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']

    # get the new page
    page = requests.get(base_url + next_page_relative_url, headers=headers)

    # parse the new page
    soup = BeautifulSoup(page.text, 'html.parser')

    scrape_page(soup, quotes)

    # look for the "Next" HTML element in the new page
    next_li_element = soup.find('li', class_='next')

csv_file = open('quotes.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
writer.writerow(['Page name','Text', 'Author', 'Tags'])

for quote in quotes:
    writer.writerow(quote.values())

csv_file.close()
