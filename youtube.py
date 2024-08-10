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
        data = dict(Channel_Name = information['snippet']['title'],
                    Channel_Id = information['id'],
                    Subscribers_Count = information['statistics']['subscriberCount'],
                    Views_Channel = information['statistics']['viewCount'],
                    Total_Videos = information['statistics']['videoCount'],
                    Channel_Description = information['snippet']['description'],
                    Playlist_Id = information['contentDetails']['relatedPlaylists']['uploads'])
    return data

Channel_Details = get_channel_info('UC5HdAapbvqWN65GIqpWWL3Q')


#print(Channel_Details)

## GET VIDEO IDS
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

all_video_ids = get_channel_video_id('UC5HdAapbvqWN65GIqpWWL3Q')"""

####  trying to get only 10 or 5 videos to use the api efficiently

all_video_ids = []

## now to get the upload id
#Call_Api_vd_id = youtube_access.channels().list(id = 'UC5HdAapbvqWN65GIqpWWL3Q',
                                                    #part = 'contentDetails').execute()
Call_Api_vd_id = youtube_access.channels().list(id = "UC5HdAapbvqWN65GIqpWWL3Q",
                                                part ='contentDetails').execute()
upload_id_vd_id = Call_Api_vd_id['items'][0]['contentDetails']['relatedPlaylists']['uploads']## got the upload id
#print(upload_id_vd_id)

get_video_ids = youtube_access.playlistItems().list(part = 'snippet', playlistId = upload_id_vd_id).execute() #, maxResults = 5)

for index in range(len(get_video_ids['items'])):
    all_video_ids.append(get_video_ids['items'][index]['snippet']['resourceId']['videoId'])

print(all_video_ids)



### get that particular channel's videos' information, using the respective video ids

def video_details_in_channel(obt_video_ids):
    video_meta_data_for_allVs = []
    for each_video_id in obt_video_ids:
        request_video_information_api = youtube_access.videos().list(part = 'snippet, ContentDetails, statistics',
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
                                    Number_Likes=item['snippet']['viewCount'] if 'viewCounts' in item['snippet'] else None,
                                    Thumbnalis = item['snippet']['thumbnails'] if 'thumbnails' in item['snippet'] else None,
                                    Description = item['snippet']['description'] if 'description' in item['snippet'] else None,
                                    Published_Date = item['snippet']['publishedAt'],
                                    Duration_Video = item['contentDetails']['duration'],
                                   Number_Views = item.get('viewCount'),
                                   Number_Comments = item.get('commentCount'),
                                   Favourite_Count = item.get('favouriteCount'),
                                   Defenition = item['contentDetails']['definition'],
                                   Caption_Status = item['contentDetails']['caption'])
                                    ## above --- :  getting the specific details using slicing
            # number_likes=item['snippet']['statistics']['viewCount']
            video_meta_data_for_allVs.append(video_meta_data)
        # print(video_meta_data_list)
    return video_meta_data_for_allVs

video_details_of_channael = video_details_in_channel(all_video_ids)


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

            print(comment_meta_data_list)

    except:
        pass

    return comment_meta_data_list

comment_meta_data_video = comment_details_videos(all_video_ids)

#print(comment_meta_data_video)


## to get details of playlist :(this set has only few playlists for limited API usage)

"""playlist_meta_data_list = []

get_playlistDetails_req_api = youtube_access.playlists().list(
                        part = 'snippet, contentDetails' ,
                        channelId = 'UC5HdAapbvqWN65GIqpWWL3Q',
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

    playlist_meta_data_list.append(playlist_details)"""



#### the complete playlist for the actual program:
def playlist_meta_data(the_channel_id):

    next_page_token_playLists = None
    playlist_meta_data_list = []

    while True:
        get_playlistDetails_req_api = youtube_access.playlists().list(
                                part = 'snippet, contentDetails' ,
                                channelId = the_channel_id, #'UC5HdAapbvqWN65GIqpWWL3Q',
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

playlists_meta_data_channel = playlist_meta_data('UC5HdAapbvqWN65GIqpWWL3Q')




