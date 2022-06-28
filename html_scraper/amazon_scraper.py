from datetime import datetime
import requests
import csv
import bs4

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5',
}

# send request to site and return site contents


def get_page_html(url):
    res = requests.get(url, headers=REQUEST_HEADER)
    return res.content


def get_product_price(soup):
    main_price_span = soup.find('span', attrs={
        'class': 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'
    })
    # could you soup.find() again for this search but using findAll to practice different methods of bs4
    price_spans = main_price_span.findAll('span')
    for span in price_spans:
        price = span.text.strip().replace('$', '').replace(',', '')
        try:
            return float(price)
        except ValueError:
            print("Value obtained for price could not be parsed")
            exit()


def get_product_title(soup):
    product_title = soup.find('span', id='productTitle')
    return product_title.text.strip()


def get_product_rating(soup):
    # get product rating that is nested in avg customer reviews
    product_ratings_div = soup.find('div', attrs={
        'id': 'averageCustomerReviews'
    })
    product_rating_section = product_ratings_div.find(
        'i', attrs={'class': 'a-icon-star'})
    product_rating_span = product_rating_section.find('span')
    try:
        rating = product_rating_span.text.strip().split()  # split rating text into a list
        return float(rating[0])  # grab first item of list that contains rating
    except ValueError:
        print("Value obtained for rating could not be parsed")
        exit()

# extract site content


def extract_product_info(url):
    product_info = {}
    print(f'Scraping url: {url}')
    html = get_page_html(url=url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    product_info['price'] = get_product_price(soup)
    product_info['title'] = get_product_title(soup)
    product_info['rating'] = get_product_rating(soup)
    print(product_info)


if __name__ == "__main__":
    with open('amazon_products_urls.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            url = row[0]
            print(extract_product_info(url))
