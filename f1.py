# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 12:06:24 2023

@author: LOGANATHAN
"""

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import snscrape.modules.twitter as sntwitter
import pymongo
from pprint import pprint
from pandas import DataFrame


title = st.text_input('Keyword to search')
st.write('keyword is', title)

title1 = st.number_input('No of tweets ')
st.write('tweets:', title1)

start = st.date_input(label='Start: ',
              value=datetime.datetime(year=2023, month=1, day=1, hour=16, minute=30),
              key='#start',
              help="The start date time",
                      on_change=lambda : None)

end = st.date_input(label='End: ',
              value=datetime.datetime(year=2023, month=5, day=30, hour=16, minute=30),
              key='#end',
              help="The end date time",
                    on_change=lambda : None)
st.write('Start: ', start, "End: ", end)

if st.button("submit"):
    
    # Creating list to append tweet data 
    tweets_list1 = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('{} since:{} until:{}'.format(title,start,end)).get_items()):
        if i>title1 : #number of tweets you want to scrape
            break
        tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username]) #declare the attributes to be returned
        
        # Creating a dataframe from the tweets list above 
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
    #displaying dataframe in streamlit    
    st.write(tweets_df1)
    #rename the column name 
    tweets_df1.rename(columns = {'Datetime':'Scraped Date'}, inplace = True)
    tweets_df1.rename(columns = {'Tweet Id':'Scraped Tweet Id'}, inplace = True)
    tweets_df1.rename(columns = {'Text':'Scraped Text'}, inplace = True)
    tweets_df1.rename(columns = {'Username':'Scraped Username'}, inplace = True)
    
    # saving the dataframe
    tweets_df1.to_csv('file1.csv')
    
   
    

        
if st.button("upload"):  
        # Load csv dataset
        data = pd.read_csv('file1.csv')
        #connecting Mongodb
        client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        #creating database
        db= client["project1"]
        #creating collection
        collection = db['demo1']
        
        data.reset_index(inplace=True)
        data_dict = data.to_dict("records")
        # Insert collection
        x=collection.insert_many(data_dict)
        print(x.inserted_ids)
        st.write("uploaded sucess")
else :
        st.write("check connection")    
        
datafile = pd.read_csv('file1.csv')
convert = datafile.to_csv(index=False).encode("utf-8")
file_name = "excel.xlsx"
st.download_button(
                label="Download data as CSV",
                data=convert,
                file_name='datacsv.csv',
                mime='text/csv',
            )


datafile = pd.read_csv('file1.csv') 
convert1 = datafile.to_json()
file_name = "excel.xlsx"
st.download_button(
                label="Download data as json",
                data=convert1,
                file_name='datajson.json',
                mime='text/csv',
            )