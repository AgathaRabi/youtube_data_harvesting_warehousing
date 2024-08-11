#  streamlit installed

# print("Hello World")  # test

#  API KEY CREATED - IS BELOW
# "AIzaSyD_GoAklQv0-JaNW4HVOzJlScGhZPjUtoU"

# next step is accessing data from you-tube
    # for that we need to write a function
        # before that get the needed packages

# downloading the package that would make the API key work

# importing the above package

from googleapiclient.discovery import build
import pymongo
import psycopg2
import pandas as pd

##########################    API CONNECT   ##############################

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
                                    Video_Id = item['id'], video_title = item['snippet']['title'],
                                    Tags_Video=item['snippet']['tags'] if 'tags' in item['snippet'] else None,
                                    Number_Likes=item['statistics'].get('likeCount'),
                                    Thumbnalis = item['snippet']['thumbnails']['default']['url'], # if 'thumbnails' in item['snippet'] else None,
                                    Description = item['snippet']['description'] if 'description' in item['snippet'] else None,
                                    Published_Date = item['snippet']['publishedAt'],
                                    Duration_Video = item['contentDetails'].get('duration'),
                                   Number_Views = item['statistics'].get('viewCount'),
                                   Number_Comments = item['statistics'].get('commentCount'),
                                   Favourite_Count = item['statistics'].get('favouriteCount'),
                                   Defenition = item['contentDetails']['definition'],
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
                            "Video_Info": videos_mdata, "Comment_Information": comment_mdata})

    return "upload completed successfully"




youtube_access = Api_connect()

channel_ids_list = ["UC5HdAapbvqWN65GIqpWWL3Q", "UChGd9JY4yMegY6PxqpBjpRA",
                    "UCrgLTEHTvedDsxdQzSAFyDA", "UC5B0fGVovcbBJXQBx5kmRhQ",
                    "UCKmE9i2iW0KaqgSxVFYmZUw", "UC21vCCoVSqgB7NzZjxB9weg",
                    "UC4c3Q2ym_hYei2cipr_KNaw", "UCy1lBBbXhtfzugF_LK2b6Yw",
                    "UCqwLyQUYPBP_4CVh7AMxNOQ", "UC81IYT8EN_pliDGCWaPkyxQ"]
for each_channel_id in channel_ids_list:
    Channel_Details = get_channel_info(each_channel_id)
    all_video_ids = get_channel_video_id(each_channel_id)
    playlists_meta_data_channel = playlist_meta_data(each_channel_id)
    insert_mdb = channel_meta_data_mdb(each_channel_id)

video_details_of_channel = video_details_in_channel(all_video_ids)
comment_meta_data_video = comment_details_videos(all_video_ids)


#### now postgresql -- connecting
## table frame creation for channels

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




### getting channel table data from mongodb

ch_data_list_from_mngdb = []
data_base = client["youtube_data"]
collection1 = data_base['youtube_channel_details']

for ch_data in collection1.find({}, {"_id":0, "Channel_Information": 1}):
    ch_data_list_from_mngdb.append(ch_data["Channel_Information"])
data_frame = pd.DataFrame(ch_data_list_from_mngdb)



### inserting channel data into postgresql channel table

for index, row in data_frame.iterrows():
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
# Upasana Dance Studio : "UC81IYT8EN_pliDGCWaPkyxQ"