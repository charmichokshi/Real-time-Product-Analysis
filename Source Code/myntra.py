
#Importing libraries
import os    
import sys   
import threading
import urllib 
import urllib.request as urllib2
import smtplib
import ftplib
import datetime, time
import bs4
import re
import numpy
import random
import operator
import webbrowser
import pandas as pd
from PIL import Image
from main import *
from bs4 import BeautifulSoup as soup
from tkinter import *

#For gui frame
root=Tk()
root.title("JACker the Hacker")
frame = Frame(root, width=150, height=150)

out1=' '
out2=' '
widget = Label(root, text='Name of the product:')
widget.config(height=5, width=30)
widget.pack(expand=YES, fill=BOTH)

#Function which is called when Find Me button is pressed
def retrieve_input():
    inputValue=textBox.get("1.0","end-1c")	#the textbox value is stored in inputValue

    print("Myntra site scrapping started")
    #Generating the url of the site-myntra
    str1 = "https://www.myntra.com/amp/"	
    str2 = inputValue
    str3 = "?rows=500&p=1"

    site = str1 + str2 + str3	#combining the various parts of url
    hdr1 = {	#header for url request
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
  
    hdr = hdr1
    req = urllib2.Request(site, headers=hdr)	#requesting site and specifying a particlar header
    response = urllib2.urlopen(req)	#opening the particular site based on request
    content = response.read()		#reading the contents of the site
    response.close()

    #anchor extraction from html document
    page_soup = soup(content, "html.parser")
    xyz = page_soup.findAll("div", {"class": "productInfo"})	#storing the content of product info in xyz
    pqr = page_soup.findAll("div", {"class": "product"})	#storing the content of product in pqr

    y = len(xyz)
    a = 2

    filename = "myntra-scraped-data.csv"
    f = open(filename, "w")		#opening file scrapping_myntra.csv
    headers = "Product_name,Price,Product_Link\n"
    f.write(headers)

    while y != 0:
        for abc, ac in zip(xyz, pqr):	#for loop to run multiple variables

            product_name = abc.findAll("h4", {"class": "name-product"})   #storing the content of product info in variable xyz
            product_name = product_name[0].text.strip()		#Removing the tags
            product_name = str(product_name.encode('utf-8', 'replace'))		#Converting prduct_name to string
            product_name = product_name[1:]
            

            current_price = abc.findAll("span", {"class": "price-discounted"})
            current_price = current_price[0].text		#Removing the tags
            current_price = str(current_price.encode('utf-8', 'replace'))  # solves unicode problem DONOT REMOVE
            current_price = current_price[3:]  # Removes first three character from converted
            current_price = current_price[11:16]

            product_link = str(ac.a["href"])	#extracting the product link
            myntra_homepage = "https://www.myntra.com"
            product_link = myntra_homepage + product_link #combining the home page & product link

            data1 = product_name + "," + current_price + "," + product_link + "\n"
            f.write(data1)	#inserting the data into csv file

        if a == 100:
            site = str(site[0:-2]) + str(a)
        elif a > 100:
            site = str(site[0:-3]) + str(a)
        elif a <= 10:
            site = str(site[0:-1]) + str(
                a)  # code will crash if the no of product listed at myntra in a specific category exceeds 500000
        elif 10 < a <= 99:
            site = str(site[0:-2]) + str(a)

        a = int(a)
        a = a + 1

        hdr = hdr1
        req = urllib2.Request(site, headers=hdr)
        response = urllib2.urlopen(req)
        content = response.read()
        response.close()
        page_soup = soup(content, "html.parser")
        xyz = page_soup.findAll("div", {"class": "productInfo"})
        pqr = page_soup.findAll("div", {"class": "product"})
        y = len(xyz)

    try:
        ap = csv.reader(f, delimiter='\t')
    finally:
        f.close()  # just closing csv file so that it can be joined in next step

    df1 = pd.read_csv("myntra-scraped-data.csv")

    column = 1  # sort by price of the product
    reader = list(csv.reader(open('myntra-scraped-data.csv')))
    reader = sorted(reader, key=operator.itemgetter(1), reverse=False)
    writer = csv.writer(open('output_myntra.csv', 'w'))		#writing in the output file
    writer.writerows(reader)

    print("Myntra site scrapping completed")
    output1 = []
    output2 = []
    output3 = []
    i=0
    f = open( 'output_myntra.csv', 'r' ) #open the file in read universal mode
    for line in f:
        cells = line.split( "," )
        if i==0: #reading the first row of sorted file
            output1.append((cells[0]))
            output2.append((cells[1]))
            output3.append((cells[2]))
        i=1

    #reading the link of cheapest product
    text1=" "
    with open('output_myntra.csv', 'r') as f:
        mycsv = csv.reader(f)
        for row in mycsv:
            text1 = row[2]
            break
    webbrowser.open(text1)	#opening the link

    call_ebay(inputValue)	#scrapping ebay site & crawling flipkart site

    output11 = []
    output12 = []
    output13 = []
    i=0
    f = open( 'output_ebay.csv', 'r' ) #open the file in read universal mode
    for line in f:
        cells = line.split( "," )
        if i==0: #reading the first row of sorted file
            output11.append((cells[0]))
            output12.append((cells[1]))
            output13.append((cells[2]))
            i=1
  
    #reading the link of cheapest product
    text=" "
    with open('output_ebay.csv', 'r') as f:
        mycsv = csv.reader(f)
        for row in mycsv:
            text = row[2]
            break
    webbrowser.open(text)	#opening the link

    #Displaying output on a new window
    root2=Tk()
    root2.title("Output window")
    frame2 = Frame(root2, width=200, height=150)
    lab=Label(root2,text="Result of related search:")
    lab.pack();
    lab8=Label(root2,text=" ")
    lab8.pack();
    l1 = Label(root2,text="Best deal from myntra")
    l1.pack();
    lab1=Label(root2,text=output1)
    lab1.pack();
    lab2=Label(root2,text=output2)
    lab2.pack();
    lab3=Label(root2,text=output3)
    lab3.pack();
    lab4=Label(root2,text=" ")
    lab4.pack();
    lab9=Label(root2,text=" ")
    lab9.pack();
    l2 = Label(root2,text="Best deal from ebay")
    l2.pack();
    lab5=Label(root2,text=output11)
    lab5.pack();
    lab6=Label(root2,text=output12)
    lab6.pack();
    lab7=Label(root2,text=output13)
    lab7.pack();

    
    frame2.pack()
    mainloop()
    
   
#inserting textbox, button in the GUI  
textBox=Text(root, height=2, width=30)
textBox.pack()
lab1=Label(root,text="  ")
lab1.pack();
buttonCommit=Button(root, height=1, width=10, text="Find Me",
                    command=lambda: retrieve_input())	#calling function retrieve_input

buttonCommit.pack()

frame.pack()
mainloop()

#End of code
