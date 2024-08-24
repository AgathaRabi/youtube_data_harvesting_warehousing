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

    channel_details_obtained = CHANNELdetailsMod.get_channel_info(channel_id)  #("UC5HdAapbvqWN65GIqpWWL3Q")
    #print(channel_details_obtained)
    #columns = channel_details_obtained.keys()
    calling_values = tuple(channel_details_obtained.values())
    #print(calling_values)
    #print("hello")

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
    obt_video_ids = VIDEOidMod.get_channel_video_id('UCKmE9i2iW0KaqgSxVFYmZUw')
    video_details_call = VIDEOdetailsMod.video_details_in_channel(obt_video_ids)
    data_frame_two = pd.DataFrame(video_details_call)
    #calling_videoData_values = video_details_call
    #print(calling_videoData_values)


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

####  comment details table


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

    obt_video_ids = VIDEOidMod.get_channel_video_id('UCKmE9i2iW0KaqgSxVFYmZUw')
    comment_details_call = COMMENTdetailsMod.comment_details_videos(obt_video_ids)
    ### converting to data frame
    data_frame_three = pd.DataFrame(comment_details_call)

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





channel_id = "UCKmE9i2iW0KaqgSxVFYmZUw"

ch_data_table = channels_details_table()  ###  calling the channel details table function


vid_dets = videos_details_table()        ###  calling the video details table function

comments_table_call = comments_details_table()




#youtube_access = Api_connect()
#video_details_call = VIDEOdetailsMod.video_details_in_channel(obt_video_ids)
#data_frame_two = pd.DataFrame(video_details_call)
#print(video_details_call)
#print(data_frame_two)