"""
Module with functions that fetch channel information
"""
import pandas as pd


def get_channel_info(channel_id, api_connection):
    """
    Function to fetch channel information, given the id
    for the channel

    Parameters:
    ----------
    channel_id: str
        The id of the channel for which information needs to be fetched
    api_connection
        The API connection object

    Returns:
    -------
    The information of the channel as a dictionary
    """

    # Build the request
    channel_info_request = api_connection.channels().list(
        part="snippet, ContentDetails, statistics",
        id=channel_id
    )
    # Call & get the response from the API
    channel_info_response = channel_info_request.execute()

    # Build the response as a dictionary
    for information in channel_info_response['items']:
        channel_info = dict(Channel_Name=information['snippet']['title'],
                            Channel_Id=information['id'],
                            Subscribers_Count=information['statistics']['subscriberCount'],
                            Views_Channel=information['statistics']['viewCount'],
                            Total_Videos=information['statistics']['videoCount'],
                            Channel_Description=information['snippet']['description'],
                            Playlist_Id=information['contentDetails']['relatedPlaylists']['uploads'])

    return channel_info


def get_channels_info(channel_ids, api_connection):
    """
    Function to fetch channel information, for a given
    list of channels

    Parameters:
    ----------
    channel_ids: list
        List with the ids of channels for which information needs to be fetched
    api_connection
        The API connection object

    Returns:
    -------
    The information of the channels as a list of dictionaries
    """

    # Declare a list to hold the information of the channels
    all_channels_info = []

    for channel_id in channel_ids:
        channel_info = get_channel_info(channel_id, api_connection)
        all_channels_info.append(channel_info)

    return pd.DataFrame(all_channels_info)


def get_channel_playlist_video_ids(channel_id, api_connection):
    """
    Function to fetch the video ids of a given channel's playlist videos

    Paramters:
    ---------
    channel_id: str
        The id of the channel for which the playlist video ids
        need to be fetched
    api_connection
        The API connection object

    Returns:
    --------
    List of video ids
    """

    # create a list to upload the videos ids
    videos_ids_list = []

    # Build the playlist info request
    playlist_info = api_connection.channels().list(id=channel_id,
                                                   part='contentDetails').execute()
    upload_id = playlist_info['items'][0]['contentDetails']['relatedPlaylists']['uploads']  ## got the upload id
    upload_info = api_connection.playlistItems().list(part='snippet',
                                                      playlistId=upload_id, maxResults = 50).execute()

    for index in range(len(upload_info['items'])):
        videos_ids_list.append(upload_info['items'][index]['snippet']['resourceId']['videoId'])

    return videos_ids_list


def get_channels_playlist_video_ids(channel_ids, api_connection):
    """
    Parameters:
    ----------
    channel_ids: list.
        List with the ids of channels for which information needs to be fetched
    api_connection
        The API connection object

    Returns:
    -------
    Dictionary where key is the channel id and value is the list of video ids for that channel
    """

    channels_video_ids_list = []

    for channel_id in channel_ids:
        video_ids = get_channel_playlist_video_ids(channel_id, api_connection)
        channels_video_ids_list.append(video_ids)

    return channels_video_ids_list





















"""
# To get all page tokens:

def get_channel_playlist_video_ids(channel_id, api_connection):
    

    # create a list to upload the videos ids
    videos_ids_list = []

    # Build the playlist info request
    playlist_info = api_connection.channels().list(id=channel_id,
                                                   part='contentDetails').execute()
    upload_id = playlist_info['items'][0]['contentDetails']['relatedPlaylists']['uploads']  ## got the upload id
    get_next_page_token = None
    ## to get all video ids a while loop is used
    while True:
        upload_info = api_connection.playlistItems().list(part='snippet',
                                                          playlistId=upload_id, maxResults = 50, pageToken = get_next_page_token).execute()

        for index in range(len(upload_info['items'])):
            videos_ids_list.append(upload_info['items'][index]['snippet']['resourceId']['videoId'])
        get_next_page_token = upload_info.get('nextPageToken')
        ## to break the while loop when you reach the end of pages
        if get_next_page_token is None:
            break
    return videos_ids_list"""


####------####
"""channels_video_ids_dict = {}

   for channel_id in channel_ids:
       video_ids = get_channel_playlist_video_ids(channel_id, api_connection)
       channels_video_ids_dict[channel_id] = video_ids

   return channels_video_ids_dict"""