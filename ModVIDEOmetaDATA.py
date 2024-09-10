"""
Module with functions to fetch meta data of videos
"""
import pandas as pd

def get_videos_meta_data_for_channel(video_id, api_connection):
    """
    Function to fetch the details of videos of the channel.

    Parameters:
    ----------
    channel_id: str
        The id of the channel for which information needs to be fetched
    api_connection
        The API connection object

    Returns:
    -------
    The details of videos of the channel as a list
    """
    #video_meta_data_for_allVs = []

    request_video_information_api = api_connection.videos().list(part='snippet, contentDetails, statistics',
                                                                 id = video_id)
    get_video_details = request_video_information_api.execute()

    videos_meta_data = []

    for item in get_video_details["items"]:
        print(item)
        video_meta_data = dict(Channel_Name=item['snippet']['channelTitle'],
                               Channel_Id=item['snippet']['channelId'],
                               Video_Id=item['id'], Video_Title=item['snippet']['title'],
                               Tags_Video=item['snippet']['tags'] if 'tags' in item['snippet'] else None,
                               Number_Likes=item['statistics'].get('likeCount'),
                               Thumbnails=item['snippet']['thumbnails']['default']['url'],
                               # if 'thumbnails' in item['snippet'] else None,
                               Description=item['snippet']['description'] if 'description' in item['snippet'] else None,
                               Published_Date=item['snippet']['publishedAt'],
                               Duration_Video=item['contentDetails'].get('duration'),
                               Number_Views=item['statistics'].get('viewCount'),
                               Number_Comments=item['statistics'].get('commentCount'),
                               Favourite_Count=item['statistics'].get('favouriteCount'),
                               Definition=item['contentDetails']['definition'],
                               Caption_Status=item['contentDetails']['caption'])

        videos_meta_data.append(video_meta_data)


    return videos_meta_data


def get_videos_meta_data_for_channels(video_ids, api_connection):
    """
    Function to fetch meta data of videos for given list of channels

    Parameters:
    ----------
    channel_ids: list
        List with the ids of channels for which information needs to be fetched
    api_connection
        The API connection object

    Returns:
    -------
    Dictionary of videos meta details for channels where channel is key and video details
    is the value
    """

    #videos_meta_data_dict = {}
    videos_meta_data_list = []

    for video_id in video_ids:
        videos_meta_data = get_videos_meta_data_for_channel(video_id, api_connection)
        print(videos_meta_data)
        #videos_meta_data_dict[video_id] = videos_meta_data
        videos_meta_data_list.append(videos_meta_data)
    #return pd.DataFrame(videos_meta_data_dict)
    return pd.DataFrame(videos_meta_data_list)

def get_comments_meta_data(video_id, api_connection):
    """
    Function to fetch meta data of comments for a given video id

    Paramters:
    ---------
    video_id: str
        The id of the video for which the comment meta data
        needs to be fetched
    api_connection
        The API connection object

    Returns:
    --------
    List of comments' meta data for the video
    """

    # Build the request
    comment_meta_data_list = []
    try:
        get_next_page_token = None
        ## to get all video ids a while loop is used

        # now to get the video id, for each video at a time
        # print(total_video_ids)

        #all_comments_details = []
        request_video_comment_api = api_connection.commentThreads().list(part='snippet',
                                                                         videoId=video_id, maxResults=50,
                                                                         pageToken=get_next_page_token)
        #print('Type of response: ', type(request_video_comment_api.execute()))
        to_get_comment_details = request_video_comment_api.execute()

        while True:
            if 'nextPageToken' in to_get_comment_details:
                get_next_page_token = to_get_comment_details['nextPageToken']
                if get_next_page_token is None:
                    break
            else:
                break
        #all_comments_details.append(to_get_comment_details)
        # print(to_get_comment_details)
        for comment_detail in to_get_comment_details['items']:
            ## getting specific details using slicing
            comment_meta_data = dict(Comment_Gvn_Id=comment_detail['snippet']['topLevelComment']['id'],
                                     Video_Id=comment_detail['snippet']['topLevelComment']['snippet']['videoId'],
                                     Comment_Text=comment_detail['snippet']['topLevelComment']['snippet']['textDisplay'],
                                     Comment_Author=comment_detail['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                     Comment_Published_Date=comment_detail['snippet']['topLevelComment']['snippet']['publishedAt'])
            comment_meta_data_list.append(comment_meta_data)

    except:
        pass

    return comment_meta_data_list



def get_comments_meta_data_for_video_ids(video_ids: list, api_connection):
    """
    Function to fetch the meta data of comment for a given list of videos

    Paramters:
    ----------
    video_ids: list
        List of video ids for which comment meta details need to be fetched

    api_connection
        The API connection object

    Returns:
    --------
    Dictionary of comment details of videos where key is video id and value is list of
    comments meta data for that video
    """

    # Declare an empty dictionary to hold meta data of videos
    videos_comment_meta_data_dict = {}

    for video_id in video_ids:
        comments_meta_data = get_comments_meta_data(video_id, api_connection)
        # Add comments meta data for current video id to dictionary
        videos_comment_meta_data_dict[video_id] = comments_meta_data

    return videos_comment_meta_data_dict


