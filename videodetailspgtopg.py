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
import videoid

def video_details_in_channel(obt_video_ids):
    video_meta_data_for_allVs = []
    for each_video_id in obt_video_ids:
        request_video_information_api = videoid.youtube_access.videos().list(part = 'snippet, contentDetails, statistics',
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



obt_video_ids = videoid.get_channel_video_id('UC5HdAapbvqWN65GIqpWWL3Q')
#youtube_access = Api_connect()

video_details_call = video_details_in_channel(obt_video_ids)
data_frame_two = pd.DataFrame(video_details_call)
print(video_details_call)
print(data_frame_two)

###  video details tables and inserting data:

def videos_details_table():
    ##connect to sql
    my_data_base_conn = psycopg2.connect(host="localhost",
                                        user="postgres",
                                        password="phoenix275",
                                        database="youtube_data",
                                        port="5432")
    my_data_base_conn.autocommit = True
    row_pointer_cursor = my_data_base_conn.cursor() ## creating a cusor object


    ## for dropping tables in case of us needing to add or overwrite data
    drop_query = '''drop table if exists video_details'''
    row_pointer_cursor.execute(drop_query)
    my_data_base_conn.commit()

    create_query = '''create table if not exists video_details(Channel_Name varchar(100),
                                                           Channel_Id varchar(100),
                                                            Video_Id varchar(80) primary key,
                                                            Video_Title varchar(150),
                                                            Tags_Video text,
                                                            Number_Likes bigint,
                                                            Thumbnails varchar(200),
                                                            Description text,
                                                            Published_Date timestamp,
                                                            Duration_Video interval,
                                                            Number_Views bigint,
                                                            Number_Comments int,
                                                            Favourite_Count int,
                                                            Definition varchar(10),
                                                            Caption_Status varchar(10))'''
    row_pointer_cursor.execute(create_query)
    my_data_base_conn.commit()

    ##  iserting data thus obtained into  postgresql tables
    calling_videoData_values = video_details_call
    print(calling_videoData_values)


    ### inserting video details data into postgresql channel table
    for index, row in data_frame_two.iterrows():
        insert_query_vds = '''insert into video_details (Channel_Name,
                                                   Channel_Id,
                                                   Video_Id,
                                                   Video_Title,
                                                   Tags_Video,
                                                   Number_Likes,
                                                   Thumbnails,
                                                   Description,
                                                   Published_Date,
                                                   Duration_Video,
                                                   Number_Views,
                                                   Number_Comments,
                                                   Favourite_Count,
                                                   Definition,
                                                   Caption_Status)

                                                   values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        value_videoDetails = (row['Channel_Name'],
                              row['Channel_Id'],
                              row['Video_Id'],
                              row['Video_Title'],
                              row['Tags_Video'],
                              row['Number_Likes'],
                              row['Thumbnails'],
                              row['Description'],
                              row['Published_Date'],
                              row['Duration_Video'],
                              row['Number_Views'],
                              row['Number_Comments'],
                              row['Favourite_Count'],
                              row['Definition'],
                              row['Caption_Status'])

        row_pointer_cursor.execute(insert_query_vds, value_videoDetails)

        #row_pointer_cursor.execute(insert_query_vds, calling_videoData_values)
        my_data_base_conn.commit()

vid_dets = videos_details_table()
