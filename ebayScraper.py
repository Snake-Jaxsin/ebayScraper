'''
To Do:
1 - Make a request to ebay.com and make a request.
2 - Collect product data from each page.
3 - Collect all links of detail pages in each product.
4 - Write scraped data to CSV file.
'''

# Import libraries.
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import time

# Get the page.
def get_page(url):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15'}
    response = requests.get(url, headers=headers)
    if not response.ok:
        print('Serve responded:', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup

# Get product details.
def get_detail_data(soup):
    try:
        title = soup.find('h1').text[14:].replace('\xa0', '')
    except:
        title = ''
    try:
        try:
            p = soup.find('span', id='prcIsum').text
        except:
            p = soup.find('span', id='mm-saleDscPrc').text
        currency, price = p.split(' ')
    except:
        currency = ''
        price = ''

    try:
        try:
            availability = soup.find('span', id='qtySubTxt').text.strip(' ').replace('\n', '').replace('\t', ' ').replace('       ', '')
        except:
            availability = soup.find('span', class_='vi-qtyS vi-bboxrev-dsplblk vi-qty-vert-algn vi-qty-pur-lnk').text.strip().replace(' ', '')
    except:
        availability = ''
    try:
        condition = soup.find('div', itemprop=('itemCondition')).text
    except:
        condition = ''
    try:
        delivery_location = soup.find('span', itemprop=('availableAtOrFrom')).text
    except:
        delivery_location = ''

    try:
        bid = soup.find('div', class_=' button-column vi-bb-small-clpd-btn ').find('span', id = 'qty-test').text
    except:
        bid = ''
    try:
        try:
            delivery_price = soup.find('div', id='shSummary').find(class_='notranslate sh-fr-cst').text.replace('\n', '')
        except:
            delivery_price = soup.find('span', class_='vi-fnf-ship-txt fnfgreen').find('strong', class_='sh_gr_bld_new').text
    except:
        delivery_price = ''


# Product data dictionary.

    data = {
        'title': title,
        'currency': currency,
        'price': price,
        'availability': availability,
        'condition':  condition,
        'delivery_location':  delivery_location,
        'bid': bid,
        'delivery_price': delivery_price,
    }
    return data

# Get all index pages.
def get_index_data(soup):
    try:
        links = soup.find_all('a', class_='s-item__link')[1:]
    except:
        links = []

    urls = [item.get('href') for item in links]
    return urls
    #print(urls)

# Write Csv
def write_csv(data, url):
    with open('ebay_output.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)

        row = [data['title'], data['currency'], data['price'], data['availability'], data['condition'], data['delivery_location'], data['bid'], data['delivery_price'], url]

        writer.writerow(row)

# Main function.
def main():
    search_term = input("What product do you want to search for? ")

    url = f"https://www.ebay.com/sch/i.html?_nkw={search_term}&_pgn=1"

    products = get_index_data(get_page(url))

    for link in products:
        #next_page_text = soup.find('ul', class_="paginate").find("li", class_='paginate__item skip next')
        data = get_detail_data(get_page(link))
        write_csv(data, link)
        time.sleep(5)
        print(data, link)

if __name__ == '__main__':
    main()

    '''
            if next_page_text == "next":
                next_page_partial = soup.find('li', class_='paginate__item skip next').find_all('a')['href']
                next_page_url = url + next_page_partial
                get_page(next_page_url)
    '''