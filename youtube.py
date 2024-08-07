#streamlit installed

# print("Hello World")  # test

#  API KEY CREATED - IS BELOW
# "AIzaSyD_GoAklQv0-JaNW4HVOzJlScGhZPjUtoU"

# next step is accessing data from you-tube
    # for that we need to write a function
        # before that get the needed packages

# downloading the package that would make the API key work

# importing the above package

from googleapiclient.discovery import build

# setting the API key connection

    # creating a function

def Api_connect(): # in this, API id, API service name, API version # helps you to access yt details
    Api_Id = "AIzaSyD_GoAklQv0-JaNW4HVOzJlScGhZPjUtoU" # API key
    Api_Service_Name = "youtube"  # service name
    Api_Version = "v3"

    youtube_bld = build(Api_Service_Name, Api_Version, developerKey = Api_Id)

    return youtube_bld ## youtube_bld is the variable name

youtube_access = Api_connect()

## get channel's information

def get_channel_info(Id_Channel):
    request = youtube_access.channels().list(
                part = "snippet, ContentDetails, statistics",
                id = Id_Channel
                #id = "UC5HdAapbvqWN65GIqpWWL3Q"
    )
    response = request.execute()
    """print(response)
    print(response['items'])
    print(response['items'][0])
    print(response['items'][0]['id'])
    print(response['items'][0]['snippet']['title'])"""

    for information in response['items']:  ### here you are getting only the details you need of channel.
        data = dict(Channel_name = information['snippet']['title'],
                    Channel_Id = information['id'],
                    Subscribers_count = information['statistics']['subscriberCount'],
                    Views_channel = information['statistics']['viewCount'],
                    Total_videos = information['statistics']['videoCount'],
                    Channel_Description = information['snippet']['description'],
                    Playlist_Id = information['contentDetails']['relatedPlaylists']['uploads'])
    return data

Channel_Details = get_channel_info('UC5HdAapbvqWN65GIqpWWL3Q')

#print(Channel_Details)

## GET VIDEO IDS

## create a list to upload the videos ids

videos_ids_list = []

#Call_Api = youtube_access.Channels_plylst_Id().list(id = Id_Channel)
"""Call_Api_vd_id = youtube_access.Channels_plylst_Id().list(id = 'UC5HdAapbvqWN65GIqpWWL3Q',
                                                    part = 'contentDetails').execute()
print(Call_Api_vd_id)"""
## now to get the upload id
Call_Api_vd_id = youtube_access.channels().list(id = 'UC5HdAapbvqWN65GIqpWWL3Q',
                                                    part = 'contentDetails').execute()
#print(Call_Api_vd_id)
#playlist_id_vd_id = ['contentDetails']['relatedPlaylists']['uploads']# error
#print(Call_Api_vd_id['items'])
#print(Call_Api_vd_id['items']['contentDetails']['relatedPlaylists']['uploads']) ## error: list indices must be integer
#print(Call_Api_vd_id['items'][0]['contentDetails']['relatedPlaylists'])
#print(Call_Api_vd_id['items'][0]['contentDetails']['relatedPlaylists']['uploads'])

upload_id_vd_id = Call_Api_vd_id['items'][0]['contentDetails']['relatedPlaylists']['uploads']## got the upload id
#print(upload_id_vd_id)

#now to get the video id
get_vid_id = youtube_access.playlistItems().list(part = 'snippet', playlistId = upload_id_vd_id, maxResults = 50).execute()
#print(get_vid_id)

