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
import APIconnectMod
import CHANNELdetailsMod
import psycopg2
import pandas as pd
import streamlit as st
import APIconnectMod
import CHANNELdetailsMod
import VIDEOidMod
import VIDEOdetailsMod
import COMMENTdetailsMod
import DatabaseMod
from CHANNELidsLIST import channel_ids_list




"""channels_mdata_list = []
channels_videoIDS_list = []
for one_channel_id in channel_ids_list:
    channel_details_call = CHANNELdetailsMod.get_channel_info(one_channel_id)
    channels_mdata_list.append(channel_details_call)
    channel_videoIDS_call = VIDEOidMod.get_channel_video_id(one_channel_id)
    channels_videoIDS_list.append(channel_videoIDS_call)
"""
#print(channels_mdata_list)
#print(channels_videoIDS_list)

#video_details_call = VIDEOdetailsMod.video_details_in_channel(channels_videoIDS_list)

channels_details_table_call = DatabaseMod.channels_details_table()




