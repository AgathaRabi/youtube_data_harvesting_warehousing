# importing the needed packages

from googleapiclient.discovery import build
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
import sqlalchemy
import pymongo
import psycopg2
import pandas as pd
import streamlit as st

###  API connect

def Api_connect(): # in this, API id, API service name, API version # helps you to access yt details
    Api_Id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # API key
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


## channel details table:
def channels_details_table():
    ##connect to sql
    my_data_base_conn = psycopg2.connect(host="localhost",
                                        user="postgres",
                                        password="phoenix275",
                                        database="youtube_data",
                                        port="5432")
    my_data_base_conn.autocommit = True
    row_pointer_cursor = my_data_base_conn.cursor() ## creating a cusor object

    ###  create table

       # b4 that drop pre- existing tables
                ## for dropping tables in case of us needing to add or overwrite data
    drop_query = '''drop table if exists channels'''
    row_pointer_cursor.execute(drop_query)

         # now create the new table:

    try:
        create_query = '''create table if not exists channels(Channel_Name varchar(100),
                                                               Channel_Id varchar(80) primary key,
                                                                Subscribers_Count bigint,
                                                                Views_Channel bigint,
                                                                Total_Videos int,
                                                                Channel_Description text,
                                                                Playlist_Id varchar(80))'''
        row_pointer_cursor.execute(create_query)
        #my_data_base_conn.commit()
    except:
        print("channels tables are created")

    channel_details_obtained = get_channel_info("UC5HdAapbvqWN65GIqpWWL3Q")
    print(channel_details_obtained)
    #columns = channel_details_obtained.keys()
    calling_values = tuple(channel_details_obtained.values())
    print(calling_values)
    print("hello")

    #for i in channel_details_obtained.values():
    insert_into_sql = '''insert into channels (Channel_Name,
                                                Channel_Id,
                                                Subscribers_Count,
                                                Views_Channel,
                                                Total_Videos,
                                                Channel_Description,
                                                Playlist_Id) VALUES(%s, %s, %s, %s, %s, %s, %s);'''
    row_pointer_cursor.execute(insert_into_sql, calling_values)

    my_data_base_conn.commit()
    #my_data_base_conn.close()






channel_id = "UC5HdAapbvqWN65GIqpWWL3Q"
youtube_access = Api_connect()

ch_data_table = channels_details_table()