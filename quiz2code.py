#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 15:49:40 2021

@author: mauratoner
"""
import json
import requests
import time
import sys
from csv import writer #writing new row to csv

apikey="S9SK7NK34k62ZL6sUxKTR1phiyCaoa0d2QpsESjo"


url = "https://yfapi.net/v6/finance/quote"
querystring = {"symbols":sys.argv[1]} #sys.argv[1] will be the command line variable stock ticker
headers = {
  'x-api-key': apikey
   }
response = requests.request("GET", url, headers=headers, params=querystring) #pull data from API
#print(response.text)
response.raise_for_status()  # raises exception when not a 2xx response 
stock_json = response.json() #create json of ticker info

if stock_json['quoteResponse']['result']==[]: #what prints when the stock ticker is not known
    print('You did not provide a valid stock ticker! Please try again.') #handling erreneous input
elif response.status_code != 204: #if stock ticker is entered correctly...
    timestamp = int(stock_json['quoteResponse']['result'][0]["regularMarketTime"]) #extract current market time
    time_converted=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timestamp)) #convert time
    name=stock_json['quoteResponse']['result'][0]["shortName"] #store short name for stock
    price=str(stock_json['quoteResponse']['result'][0]["regularMarketPrice"]) #store current price
    #create output  via command line
    print("Short Name: "+ name + " \nPrice: $" + price+ "\nTime: "+ time_converted)
    #create row of data
    newrow=[stock_json['quoteResponse']['result'][0]["symbol"],time_converted,price]
    #append new row to csv file
    with open('apistocks.csv', 'a', newline='') as f_object:  
    #Pass the CSV  file object to the writer() function and pass in 'newrow'
        writer_object = writer(f_object)
        writer_object.writerow(newrow)  
        f_object.close() #close the file object 
## source for CSV code: https://www.delftstack.com/howto/python/python-append-to-csv/