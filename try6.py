#  streamlit installed

# print("Hello World")  # test

#  API KEY CREATED - IS BELOW
# "xxxxxxxxxxxxxxxxxxxxxxxxx"

# next step is accessing data from you-tube
    # for that we need to write a function
        # before that get the needed packages

# downloading the package that would make the API key work

# importing the needed package

from googleapiclient.discovery import build
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
import sqlalchemy
import pymongo
import psycopg2
import pandas as pd
import streamlit as st

def Api_connect(): # in this, API id, API service name, API version # helps you to access yt details
    Api_Id = "xxxxxxxxxxxxxxxxxxxxxxxxxxx" # API key
    Api_Service_Name = "youtube"  # service name
    Api_Version = "v3"

    youtube_bld = build(Api_Service_Name, Api_Version, developerKey = Api_Id)

    return youtube_bld ## youtube_bld is the variable name

## get channel's information through function 'get_channel_info'

def get_channel_info(channel_id):
    channel_info_request = youtube_access.channels().list(
                part = "snippet, ContentDetails, statistics",
                id = channel_id  # here we can call how many ever channels we need
    )
    channel_info_response = channel_info_request.execute()


    for information in channel_info_response['items']:  ### here you are getting only the details you need of the channel.
        data_channel = dict(Channel_Name = information['snippet']['title'],
                            Channel_Id = information['id'],
                            Subscribers_Count = information['statistics']['subscriberCount'],
                            Views_Channel = information['statistics']['viewCount'],
                            Total_Videos = information['statistics']['videoCount'],
                            Channel_Description = information['snippet']['description'],
                            Playlist_Id = information['contentDetails']['relatedPlaylists']['uploads'])

    #df_chdts = pd.DataFrame(data_channel)
    return data_channel

def channels_details_table():
    my_data_base = psycopg2.connect(host="localhost",
                                    user="postgres",
                                    password="phoenix275",
                                    database="youtube_data",
                                    port="5432")
    row_pointer_cursor = my_data_base.cursor() ## creating a cusor object

    ## for dropping tables in case of us needing to add or overwrite data

    drop_query = '''drop table if exists channels'''
    row_pointer_cursor.execute(drop_query)
    my_data_base.commit()

    try:
        create_query = '''create table if not exists channels(Channel_Name varchar(100),
                                                               Channel_Id varchar(80) primary key,
                                                                Subscribers_Count bigint,
                                                                Views_Channel bigint,
                                                                Total_Videos int,
                                                                Channel_Description text,
                                                                Playlist_Id varchar(80))'''
        row_pointer_cursor.execute(create_query)
        my_data_base.commit()
    except:
        print("channels tables are created")

    #cursor connect



    ## getting data

    aa = get_channel_info("UC5HdAapbvqWN65GIqpWWL3Q")
    data_tobe_inserted = []

    """### getting channel table - data from mongodb

    ch_data_list_from_mngdb = []
    data_base = client["youtube_data"]
    collection1 = data_base['youtube_channel_details']"""

    for ch_data in check.find({}, {"_id": 0, "Channel_Information": 1}):
        data_tobe_inserted.append(ch_data["Channel_Information"])
    data_frame_zero = pd.DataFrame(data_tobe_inserted)
    print(data_frame_zero)
    print(aa)

    ### inserting channel data into postgresql channel table

    for index, row in data_frame_zero.iterrows():
        insert_query = '''insert into channels (Channel_Name,
                                                Channel_Id,
                                                Subscribers_Count,
                                                Views_Channel,
                                                Total_Videos,
                                                Channel_Description,
                                                Playlist_Id)

                                                values(%s, %s, %s, %s, %s, %s, %s)'''

        value_ch = (row['Channel_Name'],
                    row['Channel_Id'],
                    row['Subscribers_Count'],
                    row['Views_Channel'],
                    row['Total_Videos'],
                    row['Channel_Description'],
                    row['Playlist_Id'])
        print(value_ch)
        try:
            row_pointer_cursor.execute(insert_query, value_ch)
            my_data_base.commit()

        except:
            print("channel values are already inserted")


    return


channel_id = "UC5HdAapbvqWN65GIqpWWL3Q"
youtube_access = Api_connect()

check = get_channel_info("UC5HdAapbvqWN65GIqpWWL3Q")
print(check)


