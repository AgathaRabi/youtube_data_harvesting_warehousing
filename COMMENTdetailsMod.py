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
import VIDEOidMod
import APIconnectMod
import CHANNELdetailsMod



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


#obt_video_ids = VIDEOidMod.get_channel_video_id('UCKmE9i2iW0KaqgSxVFYmZUw')
youtube_access = APIconnectMod.Api_connect()
#comment_details_call = comment_details_videos(obt_video_ids)
### converting to data frame
#data_frame_three = pd.DataFrame(comment_details_call)
#print(comment_details_call)
#print(data_frame_three)