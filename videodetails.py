from googleapiclient.discovery import build
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
import sqlalchemy
import pymongo
import psycopg2
import pandas as pd
import streamlit as st
import channeldetails
import videoid



def Api_connect(): # in this, API id, API service name, API version # helps you to access yt details
    Api_Id = "xxxxxxxxxxxxxxxxxxxxxx" # API key
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
    return data_channel

####  trying to get only 10 or 5 videos to use the api efficiently
def get_channel_video_id(current_channel_id):

    ## create a list to upload the videos ids
    videos_ids_list = []

    ## now to get the upload id
    Call_Api_vd_id = youtube_access.channels().list(id = current_channel_id,
                                                    part ='contentDetails').execute()
    upload_id_vd_id = Call_Api_vd_id['items'][0]['contentDetails']['relatedPlaylists']['uploads']## got the upload id
    get_video_ids = youtube_access.playlistItems().list(part = 'snippet', playlistId = upload_id_vd_id).execute() #, maxResults = 5)

    for index in range(len(get_video_ids['items'])):
        videos_ids_list.append(get_video_ids['items'][index]['snippet']['resourceId']['videoId'])

    return videos_ids_list

## GET all VIDEO IDS

"""def get_channel_video_id(current_channel_id):
    ## create a list to upload the videos ids

    videos_ids_list = []

    ## now to get the upload id
    #Call_Api_vd_id = youtube_access.channels().list(id = 'UC5HdAapbvqWN65GIqpWWL3Q',
                                                        #part = 'contentDetails').execute()
    Call_Api_vd_id = youtube_access.channels().list(id = current_channel_id,
                                                    part ='contentDetails').execute()
    upload_id_vd_id = Call_Api_vd_id['items'][0]['contentDetails']['relatedPlaylists']['uploads']## got the upload id
    #print(upload_id_vd_id)
    ##  get next page token so that all video ids can be retrieved
    get_next_page_token = None
    ## to get all video ids a while loop is used
    while True:
        #now to get the video id, for each video at a time
        get_vid_id = youtube_access.playlistItems().list(part = 'snippet', playlistId = upload_id_vd_id, maxResults = 50, pageToken = get_next_page_token ).execute()
        #print(get_vid_id)

        for index in range(len(get_vid_id['items'])):
            videos_ids_list.append(get_vid_id['items'][index]['snippet']['resourceId']['videoId']) # will get only first video id

        get_next_page_token = get_vid_id.get('nextPageToken')
        ## to break the while loop when you reach the end of pages
        if get_next_page_token is None:
            break
    #print(len(videos_ids_list))
    #print(videos_ids_list)
    return videos_ids_list"""

#all_video_ids = get_channel_video_id('UC5HdAapbvqWN65GIqpWWL3Q')



channel_id = "UC5HdAapbvqWN65GIqpWWL3Q"
youtube_access = Api_connect()


def video_details_in_channel(obt_video_ids):
    video_meta_data_for_allVs = []
    for each_video_id in obt_video_ids:
        request_video_information_api = youtube_access.videos().list(part = 'snippet, contentDetails, statistics',
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



obt_video_ids = get_channel_video_id('UC5HdAapbvqWN65GIqpWWL3Q')
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
