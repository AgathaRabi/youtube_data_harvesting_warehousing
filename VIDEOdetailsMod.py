from googleapiclient.discovery import build
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
import sqlalchemy
import pymongo
import psycopg2
import pandas as pd
import streamlit as st
#import channeldetails
import VIDEOidMod

def video_details_in_channel(obt_video_ids):
    video_meta_data_for_allVs = []
    for each_video_id in obt_video_ids:
        request_video_information_api = VIDEOidMod.youtube_access.videos().list(part = 'snippet, contentDetails, statistics',
                                                                     id = each_video_id)
        get_video_details = request_video_information_api.execute()

        for item in get_video_details["items"]:
            video_meta_data = dict(Channel_Name = item['snippet']['channelTitle'],
                                    Channel_Id = item['snippet']['channelId'],
                                    Video_Id = item['id'], Video_Title = item['snippet']['title'],
                                    Tags_Video=item['snippet']['tags'] if 'tags' in item['snippet'] else None,
                                    Number_Likes=item['statistics'].get('likeCount'),
                                    Thumbnails = item['snippet']['thumbnails']['default']['url'], # if 'thumbnails' in item['snippet'] else None,
                                    Description = item['snippet']['description'] if 'description' in item['snippet'] else None,
                                    Published_Date = item['snippet']['publishedAt'],
                                    Duration_Video = item['contentDetails'].get('duration'),
                                   Number_Views = item['statistics'].get('viewCount'),
                                   Number_Comments = item['statistics'].get('commentCount'),
                                   Favourite_Count = item['statistics'].get('favouriteCount'),
                                   Definition = item['contentDetails']['definition'],
                                   Caption_Status = item['contentDetails']['caption'])
                                    ## above --- :  getting the specific details using slicing
            # number_likes=item['snippet']['statistics']['viewCount']
            video_meta_data_for_allVs.append(video_meta_data)

    return video_meta_data_for_allVs

derived_video_ids = VIDEOidMod.get_channel_video_id('UCKmE9i2iW0KaqgSxVFYmZUw')

#call = video_details_in_channel(derived_video_ids) ## test
#print(call)   ##   test