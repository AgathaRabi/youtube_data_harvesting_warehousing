#  streamlit installed

# print("Hello World")  # test

#  API KEY CREATED - IS BELOW
# "AIzaSyD_GoAklQv0-JaNW4HVOzJlScGhZPjUtoU"

# next step is accessing data from you-tube
    # for that we need to write a function
        # before that get the needed packages

# downloading the package that would make the API key work

# importing the needed package

from googleapiclient.discovery import build
import pymongo
import psycopg2
import pandas as pd
import streamlit as st


# setting the API key connection

    # creating a function for API connect

def Api_connect(): # in this, API id, API service name, API version # helps you to access yt details
    Api_Id = "AIzaSyD_GoAklQv0-JaNW4HVOzJlScGhZPjUtoU" # API key
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
    """print(response)
    print(response['items'])
    print(response['items'][0])
    print(response['items'][0]['id'])
    print(response['items'][0]['snippet']['title'])"""

    for information in channel_info_response['items']:  ### here you are getting only the details you need of the channel.
        data = dict(Channel_Name = information['snippet']['title'],
                    Channel_Id = information['id'],
                    Subscribers_Count = information['statistics']['subscriberCount'],
                    Views_Channel = information['statistics']['viewCount'],
                    Total_Videos = information['statistics']['videoCount'],
                    Channel_Description = information['snippet']['description'],
                    Playlist_Id = information['contentDetails']['relatedPlaylists']['uploads'])
    return data


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
    return videos_ids_list

all_video_ids = get_channel_video_id('UChGd9JY4yMegY6PxqpBjpRA')"""


####  trying to get only 10 or 5 videos to use the api efficiently
def get_channel_video_id(current_channel_id):

    ## create a list to upload the videos ids
    videos_ids_list = []

    ## now to get the upload id

    Call_Api_vd_id = youtube_access.channels().list(id = current_channel_id,
                                                    part ='contentDetails').execute()
    upload_id_vd_id = Call_Api_vd_id['items'][0]['contentDetails']['relatedPlaylists']['uploads']## got the upload id
    #print(upload_id_vd_id)

    get_video_ids = youtube_access.playlistItems().list(part = 'snippet', playlistId = upload_id_vd_id).execute() #, maxResults = 5)

    for index in range(len(get_video_ids['items'])):
        videos_ids_list.append(get_video_ids['items'][index]['snippet']['resourceId']['videoId'])

    return videos_ids_list


#print(all_video_ids)

### get that particular channel's videos' information, using the respective video ids

def video_details_in_channel(obt_video_ids):
    video_meta_data_for_allVs = []
    for each_video_id in obt_video_ids:
        request_video_information_api = youtube_access.videos().list(part = 'snippet, contentDetails, statistics',
                                                                 id = each_video_id)
        get_video_details = request_video_information_api.execute()
    #print(get_video_details['items'])
    #print(get_video_details['items'][0]['snippet']['tags'])
    #print(get_video_details['items'][0]['snippet']['viewCount'])
        for item in get_video_details["items"]:
            #print(item['snippet'])
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
        # print(video_meta_data_list)
    return video_meta_data_for_allVs



###  to get the comment details

##  'science with sam' another youtube channel - to limit the api quota usage - ""
def comment_details_videos(total_video_ids):
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

            #print(comment_meta_data_list)

    except:
        pass

    return comment_meta_data_list



#### the complete playlist :

"""def playlist_meta_data(the_channel_id):

    next_page_token_playLists = None
    playlist_meta_data_list = []

    while True:
        get_playlistDetails_req_api = youtube_access.playlists().list(
                                part = 'snippet, contentDetails' ,
                                channelId = the_channel_id, #'UC5HdAapbvqWN65GIqpWWL3Q', UChGd9JY4yMegY6PxqpBjpRA
                                maxResults = 50,
                                pageToken = next_page_token_playLists
                                )
        get_playlist_details_res = get_playlistDetails_req_api.execute()

        for playlist_item in get_playlist_details_res['items']:
            playlist_details = dict(Playlist_Id = playlist_item['id'],
                                    Title = playlist_item['snippet']['title'],
                                    Channel_Id = playlist_item['snippet']['channelId'],
                                    Channel_Name = playlist_item['snippet']['channelTitle'],
                                    Playlist_Published_At = playlist_item['snippet']['publishedAt'],
                                    Number_Videos_Playlist = playlist_item['contentDetails']['itemCount'])
            playlist_meta_data_list.append(playlist_details)

        next_page_token_playLists = get_playlist_details_res.get('nextPageToken')

        if next_page_token_playLists is None:
            break

    return playlist_meta_data_list

playlists_meta_data_channel = playlist_meta_data('UChGd9JY4yMegY6PxqpBjpRA')"""



## to get details of playlist :(this set has only few playlists for limited API usage)

def playlist_meta_data(the_channel_id):

    playlist_meta_data_list = []

    get_playlistDetails_req_api = youtube_access.playlists().list(
                            part = 'snippet, contentDetails',
                            channelId = the_channel_id, #'UChGd9JY4yMegY6PxqpBjpRA',
                            maxResults = 5
                            )
    get_playlist_details = get_playlistDetails_req_api.execute()

    for playlist_item in get_playlist_details['items']:

        playlist_details = dict(Playlist_Id = playlist_item['id'],
                                Title = playlist_item['snippet']['title'],
                                Channel_Id = playlist_item['snippet']['channelId'],
                                Channel_Name = playlist_item['snippet']['channelTitle'],
                                Playlist_Published_At = playlist_item['snippet']['publishedAt'],
                                Number_Videos_Playlist = playlist_item['contentDetails']['itemCount'])

        playlist_meta_data_list.append(playlist_details)

    return playlist_meta_data_list


#print(playlists_meta_data_channel)


#####   mongodb
# connecting to mongodb

client = pymongo.MongoClient("mongodb+srv://agatha83painting:D2fFKo5qqT0RXJGG@cluster0.f57ra.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
data_base = client["youtube_data"]


# upload to mongodb
# upload channel details


def channel_meta_data_mdb(Id_Channel):
    channel_mdata = get_channel_info(Id_Channel)
    channel_video_ids = get_channel_video_id(Id_Channel)
    videos_mdata = video_details_in_channel(channel_video_ids)
    comment_mdata = comment_details_videos(channel_video_ids)
    playlists_mdata = playlist_meta_data(Id_Channel)

    collection1 = data_base['youtube_channel_details']
    collection1.insert_one({"Channel_Information": channel_mdata, "Playlist_Information": playlists_mdata,
                            "Video_Information": videos_mdata, "Comment_Information": comment_mdata})

    return "upload completed successfully"

youtube_access = Api_connect()

channel_ids_list = ["UC5HdAapbvqWN65GIqpWWL3Q", "UChGd9JY4yMegY6PxqpBjpRA",
                    "UCrgLTEHTvedDsxdQzSAFyDA", "UC5B0fGVovcbBJXQBx5kmRhQ",
                    "UCKmE9i2iW0KaqgSxVFYmZUw", "UC21vCCoVSqgB7NzZjxB9weg",
                    "UC4c3Q2ym_hYei2cipr_KNaw", "UCy1lBBbXhtfzugF_LK2b6Yw",
                    "UCqwLyQUYPBP_4CVh7AMxNOQ", "UC7cgHgo42oYABKWabReHZyA"]
for each_channel_id in channel_ids_list:
    Channel_Details = get_channel_info(each_channel_id)
    all_video_ids = get_channel_video_id(each_channel_id)
    playlists_meta_data_channel = playlist_meta_data(each_channel_id)
    insert_mdb = channel_meta_data_mdb(each_channel_id)

video_details_of_channel = video_details_in_channel(all_video_ids)
comment_meta_data_video = comment_details_videos(all_video_ids)

#### now postgresql -- connecting
## table frame creation for channels


def channels_details_table():

    my_data_base = psycopg2.connect(host = "localhost",
                                    user = "postgres",
                                    password = "phoenix275",
                                    database = "youtube_data",
                                    port = "5432")
    row_pointer_cursor = my_data_base.cursor()

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




    ### getting channel table - data from mongodb

    ch_data_list_from_mngdb = []
    data_base = client["youtube_data"]
    collection1 = data_base['youtube_channel_details']

    for ch_data in collection1.find({}, {"_id":0, "Channel_Information": 1}):
        ch_data_list_from_mngdb.append(ch_data["Channel_Information"])
    data_frame_zero = pd.DataFrame(ch_data_list_from_mngdb)



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

        try:
            row_pointer_cursor.execute(insert_query, value_ch)
            my_data_base.commit()

        except:
            print("channel values are already inserted")


###  playlist tables and inserting data: ###################
def playlists_details_table():

    # creating playlist table in postgresql:
    my_data_base = psycopg2.connect(host = "localhost",
                                    user = "postgres",
                                    password = "phoenix275",
                                    database = "youtube_data",
                                    port = "5432")
    row_pointer_cursor = my_data_base.cursor()

    ## for dropping tables in case of us needing to add or overwrite data
    drop_query = '''drop table if exists playlists'''
    row_pointer_cursor.execute(drop_query)
    my_data_base.commit()


    create_query = '''create table if not exists playlists(Playlist_Id varchar(100) primary key,
                                                           Title varchar(100),
                                                            Channel_Id varchar(100),
                                                            Channel_Name varchar(100),
                                                            Playlist_Published_At timestamp,
                                                            Number_Videos_Playlist int)'''
    row_pointer_cursor.execute(create_query)
    my_data_base.commit()


    ### getting playlists table - data from mongodb
    plylst_data_list_from_mngdb = []
    data_base = client["youtube_data"]
    collection1 = data_base['youtube_channel_details']

    for plylst_data in collection1.find({}, {"_id":0, "Playlist_Information": 1}):
        for i in range(len(plylst_data["Playlist_Information"])):
            plylst_data_list_from_mngdb.append(plylst_data["Playlist_Information"][i])

    ### converting to data frame
    data_frame_one = pd.DataFrame(plylst_data_list_from_mngdb)
    print(data_frame_one)
    ### inserting playlist data into postgresql channel table
    for index, row in data_frame_one.iterrows():
        insert_query_plylst = '''insert into playlists (Playlist_Id,
                                                       Title,
                                                       Channel_Id,
                                                       Channel_Name,
                                                       Playlist_Published_At,
                                                       Number_Videos_Playlist)
    
                                                   values(%s,%s,%s,%s,%s,%s)'''
        value_plylst = (row['Playlist_Id'],
                    row['Title'],
                    row['Channel_Id'],
                    row['Channel_Name'],
                    row['Playlist_Published_At'],
                    row['Number_Videos_Playlist'])


        row_pointer_cursor.execute(insert_query_plylst, value_plylst)
        my_data_base.commit()



###  video details tables and inserting data:

def videos_details_table():

    # creating video details table in postgresql:
    my_data_base = psycopg2.connect(host = "localhost",
                                    user = "postgres",
                                    password = "phoenix275",
                                    database = "youtube_data",
                                    port = "5432")
    row_pointer_cursor = my_data_base.cursor()

    ## for dropping tables in case of us needing to add or overwrite data
    drop_query = '''drop table if exists video_details'''
    row_pointer_cursor.execute(drop_query)
    my_data_base.commit()


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
    my_data_base.commit()


    ### getting video details table - data from mongodb
    video_data_list_from_mngdb = []
    data_base = client["youtube_data"]
    collection1 = data_base['youtube_channel_details']

    for video_data in collection1.find({}, {"_id":0, "Video_Information": 1}):
        for j in range(len(video_data["Video_Information"])):
            video_data_list_from_mngdb.append(video_data["Video_Information"][j])

    ### converting to data frame
    data_frame_two = pd.DataFrame(video_data_list_from_mngdb)

    ### inserting playlist data into postgresql channel table
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
        my_data_base.commit()

############ comments tables and inserting data: ###################

def comments_details_table():

    # creating comment_details table in postgresql:
    #connecting
    my_data_base = psycopg2.connect(host = "localhost",
                                    user = "postgres",
                                    password = "phoenix275",
                                    database = "youtube_data",
                                    port = "5432")
    row_pointer_cursor = my_data_base.cursor()

    ## for dropping tables in case of us needing to add or overwrite data
    drop_query = '''drop table if exists comment_details'''
    row_pointer_cursor.execute(drop_query)
    my_data_base.commit()


    create_query = '''create table if not exists comment_details(Comment_Gvn_Id varchar(100) primary key,
                                                                Video_Id varchar(100),
                                                                Comment_Text text,
                                                                Comment_Author varchar(150),
                                                                Comment_Published_Date timestamp)'''
    row_pointer_cursor.execute(create_query)
    my_data_base.commit()


    ### getting comment details table - data from mongodb
    comment_data_list_from_mngdb = []
    data_base = client["youtube_data"]
    collection1 = data_base['youtube_channel_details']

    for comment_data in collection1.find({}, {"_id":0, "Comment_Information": 1}):
        for k in range(len(comment_data["Comment_Information"])):
            comment_data_list_from_mngdb.append(comment_data["Comment_Information"][k])

    ### converting to data frame
    data_frame_three = pd.DataFrame(comment_data_list_from_mngdb)

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
        my_data_base.commit()

#########------calling all tables using one function---------###########

def all_tables():
    channels_details_table()
    playlists_details_table()
    videos_details_table()
    comments_details_table()

    return "tables created successfully"

all_tables_fn_call = all_tables()


#########now to display the tables  using streamlit######

## fns for streamlit:

def show_channel_details_table():
    ch_data_list_from_mngdb = []
    data_base = client["youtube_data"]
    collection1 = data_base['youtube_channel_details']

    for ch_data in collection1.find({}, {"_id": 0, "Channel_Information": 1}):
        ch_data_list_from_mngdb.append(ch_data["Channel_Information"])
    ### converting to data frame
    data_frame_zero = st.dataframe(ch_data_list_from_mngdb)

    return data_frame_zero


def show_playlist_details_table():

    ### getting playlists table - data from mongodb
    plylst_data_list_from_mngdb = []
    data_base = client["youtube_data"]
    collection1 = data_base['youtube_channel_details']

    for plylst_data in collection1.find({}, {"_id": 0, "Playlist_Information": 1}):
        for i in range(len(plylst_data["Playlist_Information"])):
            plylst_data_list_from_mngdb.append(plylst_data["Playlist_Information"][i])
    ### converting to data frame
    data_frame_one = st.dataframe(plylst_data_list_from_mngdb)

    return data_frame_one

def show_video_details_table():

    ### getting video details table - data from mongodb
    video_data_list_from_mngdb = []
    data_base = client["youtube_data"]
    collection1 = data_base['youtube_channel_details']

    for video_data in collection1.find({}, {"_id": 0, "Video_Information": 1}):
        for j in range(len(video_data["Video_Information"])):
            video_data_list_from_mngdb.append(video_data["Video_Information"][j])

    ### converting to data frame
    data_frame_two = st.dataframe(video_data_list_from_mngdb)

    return data_frame_two


def show_comment_details_table():

    ### getting comment details table - data from mongodb
    comment_data_list_from_mngdb = []
    data_base = client["youtube_data"]
    collection1 = data_base['youtube_channel_details']

    for comment_data in collection1.find({}, {"_id": 0, "Comment_Information": 1}):
        for k in range(len(comment_data["Comment_Information"])):
            comment_data_list_from_mngdb.append(comment_data["Comment_Information"][k])

    ### converting to data frame
    data_frame_three = st.dataframe(comment_data_list_from_mngdb)

    return data_frame_three


##### stream lit ------ VISUAL PAGE---###########

with st.sidebar:
    st.title(":blue[YOUTUBE DATA HARVESTING AND WAREHOUSING]")
    st.header("Skill Take Away")
    st.caption("Python Scripting")
    st.caption("Data Collection")
    st.caption("MongoDB")
    st.caption("API Integration")
    st.caption("Data Management using MongoDB and SQL")

channel_id_streamlit = st.text_input("Enter the Channel ID")

if st.button("collect and store data"):  ## theses coming lines are to avoid repetitive channel id data in MongoDB
    ch_ids = []
    data_base = client["youtube_data"]
    collection1 = data_base['youtube_channel_details']

    for ch_data in collection1.find({}, {"_id": 0, "Channel_Information": 1}):
        ch_ids.append(ch_data["Channel_Information"]["Channel_Id"])## collecting all channel ids in mongo db into ch_ids

    if channel_id_streamlit in ch_ids:
        st.success("Channel details for the given Channel ID already exists")
    else:
        insert_to_mdb = channel_meta_data_mdb(channel_id_streamlit) # if not repetitive insert into MongoDB using already created function(channel_meta_data_mdb)
        st.success(insert_to_mdb)

if st.button("Migrate to SQL"):
    tables_for_newid = all_tables()
    st.success(tables_for_newid)

#### radio

show_tables_list = st.radio("SELECT THE TABLE FOR VIEW",("CHANNEL DETAILS", "PLAYLIST DETAILS", "VIDEO DETAILS", "COMMENT DETAILS"))

## appropriate show table functions to be called for the choice made:
if show_tables_list == "CHANNEL DETAILS":
    show_channel_details_table()

elif show_tables_list == "PLAYLIST DETAILS":
    show_playlist_details_table()

elif show_tables_list == "VIDEO DETAILS":
    show_video_details_table()

elif show_tables_list == "COMMENT DETAILS":
    show_comment_details_table()


##   SQL Connection in streamlit for the list of speicified queries:

## sql connection
my_data_base = psycopg2.connect(host = "localhost",
                                user = "postgres",
                                password = "phoenix275",
                                database = "youtube_data",
                                port = "5432")
row_pointer_cursor = my_data_base.cursor()

question = st.selectbox("Select your Question",("1. All the videos and the Channel name",
                                                "2. Channels with the most number of videos",
                                                "3. 10 most viewed videos",
                                                "4. Comments in each channel",
                                                "5. Videos with highest likes"
                                                "6. Likes of all videos",
                                                "7. Views of each channel",
                                                "8. Videos published in the year of 2022",
                                                "9. average duration of videos in each channel",
                                                "10. videos with the highest number of comments"))

# import

# all functions defined

# 1 Get api connection

# 2 Declare list of channel ids

# 3 For each channel id, get channel details and put the results in a list

# 4 For each channel detail, get video id and with video id, get video details and comment details

# 5 For each channel id, get playlist details

# 6 Connect to Mongo DB

# 7 Upload to Mongo DB and get

# 8 Connect to local postgres

# 9 Send to steam lit


### list of channels from which you want to get data

#  charlie follows : "UC5HdAapbvqWN65GIqpWWL3Q"
# science with sam : "UChGd9JY4yMegY6PxqpBjpRA"
# ducatidreams     : "UCrgLTEHTvedDsxdQzSAFyDA"
# HARISH THYGARAJAN : "UC5B0fGVovcbBJXQBx5kmRhQ"
#  music academy of madras : "UCKmE9i2iW0KaqgSxVFYmZUw"
# Apoorva Jayaraman :"UC21vCCoVSqgB7NzZjxB9weg"
#  RAM TRB ACADEMY : "UC4c3Q2ym_hYei2cipr_KNaw"
#  tamil business podcast:"UCy1lBBbXhtfzugF_LK2b6Yw"
# MATHURALAYA SCHOOL OF DANCE : "UCqwLyQUYPBP_4CVh7AMxNOQ"
# Josephine Nithya : "UC7cgHgo42oYABKWabReHZyA"

#"""("1. What are the names of all the videos and their corresponding channels?",
#                                                "2. Which channels have the most number of videos, and how many videos do they have?" ,
#                                                "3. What are the top 10 most viewed videos and their respective channels?",
#                                                "4. How many comments were made on each video, and what are their  corresponding video names?",
#                                                "5. Which videos have the highest number of likes, and what are their corresponding channel names?"
#                                                "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
#                                                "7. What is the total number of views for each channel, and what are their  corresponding channel names?",
#                                                "8. What are the names of all the channels that have published videos in the year  2022?",
#                                                "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
#                                                "10. Which videos have the highest number of comments, and what are their  corresponding channel names?")"""