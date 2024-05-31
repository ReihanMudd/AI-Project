from requests_html import HTMLSession
import pandas as pd
from tqdm import tqdm

import google.generativeai as genai

s = HTMLSession()

data = []

def basic():
    url = input("Enter your link: ")
    r = s.get(url)
    content = r.html.find('li.s-item')
    for item in tqdm(content):
        title_element = item.find('div.s-item__title', first=True)
        title = title_element.text if title_element else ''

        subtitle_element = item.find('div.s-item__subtitle', first=True)
        subtitle = subtitle_element.text if subtitle_element else ''

        price_element = item.find('span.s-item__price', first=True)
        price = price_element.text if price_element else ''

        discountprice_element = item.find('span.s-item__discount', first=True)
        discountprice = discountprice_element.text if discountprice_element else ''

        shippingprice_element = item.find('span.s-item__logisticsCost', first=True)
        shippingprice = shippingprice_element.text.replace('shipping', '') if shippingprice_element else ''

        shippingfrom_element = item.find('span.s-item__location', first=True)
        shippingfrom = shippingfrom_element.text.replace('from', '') if shippingfrom_element else ''

        url_element = item.find('a.s-item__link', first=True)
        url = url_element.attrs['href'] if url_element else ''

        data.append([title, subtitle, price, discountprice, shippingprice, shippingfrom, url])

    df = pd.DataFrame(data, columns=['Title', 'Sub Title', 'Price', 'Discount Price', 'Shipping Price', 'Shipping From', 'URL'])
    df.to_csv('Ebay dataset.csv', index=False)
    
"""""
def keyworded():
    keyword = input("Enter your keyword here: ")
    urls = ['https://www.ebay.com/sch/i.html?_from=R40&_nkw={}&_sacat=0&_pgn={}'.format(keyword, x) for x in range(1,6)]
    for url in tqdm(urls):
        r = s.get(url)
        content = r.html.find('li.s-item')
        for item in tqdm(content):
            title_element = item.find('div.s-item__title', first=True)
            title = title_element.text if title_element else ''

            subtitle_element = item.find('div.s-item__subtitle', first=True)
            subtitle = subtitle_element.text if subtitle_element else ''

            price_element = item.find('span.s-item__price', first=True)
            price = price_element.text if price_element else ''

            discountprice_element = item.find('span.s-item__discount', first=True)
            discountprice = discountprice_element.text if discountprice_element else ''

            shippingprice_element = item.find('span.s-item__logisticsCost', first=True)
            shippingprice = shippingprice_element.text.replace('shipping', '') if shippingprice_element else ''

            shippingfrom_element = item.find('span.s-item__location', first=True)
            shippingfrom = shippingfrom_element.text.replace('from', '') if shippingfrom_element else ''

            url_element = item.find('a.s-item__link', first=True)
            url = url_element.attrs['href'] if url_element else ''

            data.append([title, subtitle, price, discountprice, shippingprice, shippingfrom, url])

        df = pd.DataFrame(data, columns=['Title', 'Sub Title', 'Price', 'Discount Price', 'Shipping Price', 'Shipping From', 'URL'])
        df.to_csv(f'{keyword}.csv', index=False, mode='a', header=False)
        data.clear()
"""""


genai.configure(api_key="AIzaSyAp1Xt0TNgKXwu_ll8rigDiAFRipu0QBVg")
basic()