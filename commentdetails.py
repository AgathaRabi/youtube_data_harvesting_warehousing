from googleapiclient.discovery import build
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
import sqlalchemy
import pymongo
import psycopg2
import pandas as pd
import streamlit as st
#import channelid



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



channel_id = "UC7cgHgo42oYABKWabReHZyA"
youtube_access = Api_connect()


obt_video_ids = get_channel_video_id('UC7cgHgo42oYABKWabReHZyA')
#youtube_access = Api_connect()



"""def comment_details_videos(total_video_ids):
    comment_meta_data_list =[]
    try:
        for every_video_id in total_video_ids:
            request_video_comment_api =youtube_access.commentThreads().list(part = 'snippet',
                                                                         videoId = every_video_id, maxResults = 50)
            to_get_comment_details = request_video_comment_api.execute()
            for comment_detail in to_get_comment_details['items']:
                ## getting specific details using slicing
                comment_meta_data = dict(Comment_Gvn_Id = comment_detail['snippet']['topLevelComment']['id'],
                                         Video_Id = comment_detail['snippet']['topLevelComment']['snippet']['videoId'],
                                         Comment_Text = comment_detail['snippet']['topLevelComment']['snippet']['textDisplay'],
                                         Comment_Author = comment_detail['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                         Comment_Published_Date = comment_detail['snippet']['topLevelComment']['snippet']['publishedAt'])
                comment_meta_data_list.append(comment_meta_data)


    except:
        pass

    return comment_meta_data_list"""

#####   GET ALL COMMENTS AND HENCE THEIR DETAILS:

def comment_details_videos(total_video_ids): ## all comments
    comment_meta_data_list =[]
#try:
    get_next_page_token = None
    ## to get all video ids a while loop is used

    #now to get the video id, for each video at a time
    #print(total_video_ids)
    for every_video_id in total_video_ids:
        all_comments_details = []
        request_video_comment_api = youtube_access.commentThreads().list(part = 'snippet',
                                                                    videoId = every_video_id, maxResults = 50,
                                                                    pageToken = get_next_page_token)
        print('Type of response: ', type(request_video_comment_api.execute()))
        to_get_comment_details = request_video_comment_api.execute()
        print(every_video_id)
        while True:
            if 'nextPageToken' in to_get_comment_details:
                get_next_page_token = to_get_comment_details['nextPageToken']
                if get_next_page_token is None:
                    break
            else: break
        all_comments_details.append(to_get_comment_details)
        #print(to_get_comment_details)
        for comment_detail in to_get_comment_details['items']:
            ## getting specific details using slicing
            comment_meta_data = dict(Comment_Gvn_Id = comment_detail['snippet']['topLevelComment']['id'],
                                     Video_Id = comment_detail['snippet']['topLevelComment']['snippet']['videoId'],
                                     Comment_Text = comment_detail['snippet']['topLevelComment']['snippet']['textDisplay'],
                                     Comment_Author = comment_detail['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                     Comment_Published_Date = comment_detail['snippet']['topLevelComment']['snippet']['publishedAt'])
            comment_meta_data_list.append(comment_meta_data)


#except:
    #pass

    return comment_meta_data_list




comment_details_call = comment_details_videos(obt_video_ids)
### converting to data frame
data_frame_three = pd.DataFrame(comment_details_call)
#print(comment_details_call)
#print(data_frame_three)

def comments_details_table():
    # creating comment_details table in postgresql:
    # connecting
    my_data_base_conn = psycopg2.connect(host="localhost",
                                    user="postgres",
                                    password="phoenix275",
                                    database="youtube_data",
                                    port="5432")
    my_data_base_conn.autocommit = True
    row_pointer_cursor = my_data_base_conn.cursor()  ## creating a cusor object

    ## for dropping tables in case of us needing to add or overwrite data
    drop_query = '''drop table if exists comment_details'''
    row_pointer_cursor.execute(drop_query)
    my_data_base_conn.commit()

    create_query = '''create table if not exists comment_details(Comment_Gvn_Id varchar(100) primary key,
                                                                Video_Id varchar(100),
                                                                Comment_Text text,
                                                                Comment_Author varchar(150),
                                                                Comment_Published_Date timestamp)'''
    row_pointer_cursor.execute(create_query)
    my_data_base_conn.commit()



    ### inserting playlist data into postgresql channel table
    for index, row in data_frame_three.iterrows():
        insert_query_commentdts = '''insert into comment_details (Comment_Gvn_Id,
                                                                Video_Id,
                                                                Comment_Text,
                                                                Comment_Author,
                                                                Comment_Published_Date)

                                                   values(%s, %s, %s, %s, %s)'''
        value_commentdts = (row['Comment_Gvn_Id'],
                            row['Video_Id'],
                            row['Comment_Text'],
                            row['Comment_Author'],
                            row['Comment_Published_Date'])

        row_pointer_cursor.execute(insert_query_commentdts, value_commentdts)
        my_data_base_conn.commit()

comments_table_call = comments_details_table()



#### getting all comments -- TRIAL 1
"""
def comment_details_videos(total_video_ids): ## all comments
    comment_meta_data_list =[]
#try:
    get_next_page_token = None
    ## to get all video ids a while loop is used

    #now to get the video id, for each video at a time
    #print(total_video_ids)
    for every_video_id in total_video_ids:
        while True:
            request_video_comment_api = youtube_access.commentThreads().list(part = 'snippet',
                                                                        videoId = every_video_id, maxResults = 50,
                                                                        pageToken = get_next_page_token)
            print('Type of response: ', type(request_video_comment_api.execute()))
            to_get_comment_details = request_video_comment_api.execute()
            print(every_video_id)
            if get_next_page_token is None:
                break
        #print(to_get_comment_details)
        for comment_detail in to_get_comment_details['items']:
            ## getting specific details using slicing
            comment_meta_data = dict(Comment_Gvn_Id = comment_detail['snippet']['topLevelComment']['id'],
                                     Video_Id = comment_detail['snippet']['topLevelComment']['snippet']['videoId'],
                                     Comment_Text = comment_detail['snippet']['topLevelComment']['snippet']['textDisplay'],
                                     Comment_Author = comment_detail['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                     Comment_Published_Date = comment_detail['snippet']['topLevelComment']['snippet']['publishedAt'])
            comment_meta_data_list.append(comment_meta_data)
        get_next_page_token = to_get_comment_details['nextPageToken']

#except:
    #pass

    return comment_meta_data_list"""