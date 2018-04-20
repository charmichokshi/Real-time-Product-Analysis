from lxml import html
import requests
from pprint import pprint
import csv
from traceback import format_exc
import argparse


def parse(brand):
    for i in range(5):
        try:
            url = 'http://www.ebay.com/sch/i.html?_nkw={0}&_sacat=0'.format(brand)
            print
            "Retrieving %s" % (url)
            response = requests.get(url)
            print
            "Parsing page"
            parser = html.fromstring(response.text)
            product_listings = parser.xpath('//li[contains(@class,"lvresult")]')
            raw_result_count = parser.xpath("//span[@class='rcnt']//text()")
            result_count = ''.join(raw_result_count).strip()
            print
            "Found {0} results for {1}".format(result_count, brand)
            scraped_products = []

            for product in product_listings:
                raw_url = product.xpath('.//a[@class="vip"]/@href')
                raw_title = product.xpath('.//a[@class="vip"]/text()')
                raw_price = product.xpath(".//li[contains(@class,'lvprice')]//span[@class='bold']//text()")
                price = ' '.join(' '.join(raw_price).split())
                title = ' '.join(' '.join(raw_title).split())
                data = {
                    'url': raw_url[0],
                    'title': title,
                    'price': price
                }
                scraped_products.append(data)
            return scraped_products
        except Exception as e:
            print
            format_exc(e)


if __name__ == "__main__":

    brand = " "
    with open('%s-ebay-scraped-data.csv' % (brand), 'w') as csvfile:
        fieldnames = ["title", "price", "url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for data in scraped_data:
            writer.writerow(data)
