from requests_html import HTMLSession
import pandas as pd
from tqdm import tqdm
import google.generativeai as genai
import os
from AI import *

s = HTMLSession()

data = []


def keyworded(keyword):
    urls = ['https://www.ebay.com/sch/i.html?_from=R40&_nkw={}&_sacat=0&_pgn={}'.format(keyword, x) for x in range(1,10)]
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

def main():
    genai.configure(api_key="AIzaSyAp1Xt0TNgKXwu_ll8rigDiAFRipu0QBVg")
    model = genai.GenerativeModel('gemini-1.5-pro')

    trendy = ['iphone', 'samsung', 'sony', 'lg', 'laptop', 'jordans', 'playstation', 'xbox', 'console', 'headphones', 'airpods', 'phone', 'shoes', 'gucci', 'designer', 'tv', 'coach', 'louis Vuitton', 'nike', 'accessories', 'watch', 'purse', 'wallet', 'sunglasses', 'phone case', 'earbuds', 'speaker', 'camera']

    # Create a folder to store the combined CSV file
    output_folder = os.path.join(os.getcwd(), 'output_data')
    os.makedirs(output_folder, exist_ok=True)

    # Initialize an empty DataFrame to store the combined data
    combined_data = pd.DataFrame()

    for keyword in trendy:
        keyworded(keyword)
        
        # Read the CSV file for the current keyword
        csv_file = f'{keyword}.csv'
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            
            # Append the data to the combined DataFrame
            combined_data = pd.concat([combined_data, df], ignore_index=True)
            
            # Delete the individual CSV file
            os.remove(csv_file)

    # Save the combined DataFrame to a CSV file in the output folder
    output_file = os.path.join(output_folder, 'combined_data.csv')
    combined_data.to_csv(output_file, index=False)

    print("Welcome to the awesome interactive EBAY shop!")

    get_response("Who are you?")

main()