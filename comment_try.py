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
    Api_Id = "xxxxxxxxxxxxxxxxxxxxxxxxxxx" # API key
    Api_Service_Name = "youtube"  # service name
    Api_Version = "v3"

    youtube_bld = build(Api_Service_Name, Api_Version, developerKey = Api_Id)

    return youtube_bld ## youtube_bld is the variable name

channel_id = "UC5HdAapbvqWN65GIqpWWL3Q"
youtube_access = Api_connect()

## get channel's information through function 'get_channel_info'

#def get_channel_info(channel_id):
channel_info_request = youtube_access.channels().list(
            part = "snippet, ContentDetails, statistics",
            id = channel_id  # here we can call how many ever channels we need
)
channel_info_response = channel_info_request.execute()


print(channel_info_response)
