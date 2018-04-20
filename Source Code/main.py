
#Importing libraries
import csv
import threading
import operator
import itertools
import requests
from lxml import html
from tkinter import *
from domain import *
from general import *
from spider import Spider
from queue import Queue
from traceback import format_exc

def call_ebay(inputValue):

    print("ebay site scrapping started")
    #scrapping ebay site
    def parse(brand):	#here brand is a surched product's name
        for i in range(5):	#loop will iteraye maximum of 5 times (useful in the case of exception)
            try:
                url = 'http://www.ebay.com/sch/i.html?_nkw={0}&_sacat=0'.format(brand)   #URL syntex of ebay.com
                print
                "Retrieving %s" % (url)		#printing retrived url
                response = requests.get(url)
                print
                "Parsing page"	#printing parsed page
                parser = html.fromstring(response.text)
                product_listings = parser.xpath('//li[contains(@class,"lvresult")]') #passing value of lvresult to product_listings 
                raw_result_count = parser.xpath("//span[@class='rcnt']//text()")     #passing value of rcnt to raw_result_count 
                result_count = ''.join(raw_result_count).strip()
                print
                "Found {0} results for {1}".format(result_count, brand)
                scraped_products = []

		#same as above as product_listing
                for product in product_listings:
                    raw_url = product.xpath('.//a[@class="vip"]/@href')
                    raw_title = product.xpath('.//a[@class="vip"]/text()')
                    raw_price = product.xpath(".//li[contains(@class,'lvprice')]//span[@class='bold']//text()")
                    price = ' '.join(' '.join(raw_price).split())
                    price = price[1:]
                    
                    price_temp = " "
                    for char in price:
                        if char == " ":		#removing the blank space from price variable
                            break
                        elif char == ',':	#removing the coma from price variable
                            price_temp=price_temp
                        else:
                            price_temp=price_temp+char

                    price=price_temp	
                    
                    price1 = float(price) #converting price string to flot
                    price1 = price1*64.58	#converting price of product from $ to INR
                    
                    title = ' '.join(' '.join(raw_title).split())

                    data = {		#assigning data
                        'url': raw_url[0],
                        'title': title,
                        'price ($)': price1
                    }
                    scraped_products.append(data)
                return scraped_products	  #returning the scarpped data
            except Exception as e:	#in case of exception, this part of code will get executed
                print
                format_exc(e)  #print stack traces under program control


    scraped_data = parse(inputValue)	#scraped_data will have returned values of function parse

    print
    "Writing scraped data to ebay-scraped-data.csv"

    #inserting scraped data into ebay-scraped-data file 
    with open('ebay-scraped-data.csv' , 'w') as csvfile:
        fieldnames = ["title", "price ($)", "url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for data in scraped_data:
            writer.writerow(data)

    #sorting scraped data into output_ebay file 
    column = 1
    reader = list(csv.reader(open('ebay-scraped-data.csv')))
    reader = sorted(reader, key=lambda row: row[1], reverse=False)
    writer = csv.writer(open('output_ebay.csv', 'w'))
    writer.writerows(reader)
    print("ebay site scrapping started")

