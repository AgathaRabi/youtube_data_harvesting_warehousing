"""
The main module of the program
"""
from googleapiclient.discovery import build
import ModCHANNELSdetails
import ModVIDEOmetaDATA
import ModDATABASEinterface as db_int
import sys


def run(api_key, pre_def_channel_ids):
    """
    The main function that runs the youtube data harvesting and wareshousing program.

    api_key: str
        The api key to get the API connection object

    pre_def_channel_ids: list
        List of pre defined channels to fetch the data from API and save to database
    """

    # Get the local DB connection
    db_conn = db_int.get_local_db_conn()

    # Drop and create fresh tables
    db_int.drop_and_create_channel_dets_table(db_conn)
    db_int.drop_and_create_video_dets_table(db_conn)
    db_int.drop_and_create_comment_dets_table(db_conn)

    # Get the API connection
    api_connection = get_youtube_api_conn(api_key)

    # Get and store information for the pre-defined list of channel ids

    # Get the channel details for the pre defined list of channel ids
    channels_info = ModCHANNELSdetails.get_channels_info(pre_def_channel_ids, api_connection)

    # Get the video ids for the channels playlist
    channels_video_ids_dict = ModCHANNELSdetails.get_channels_playlist_video_ids(pre_def_channel_ids,
                                                                                     api_connection)
    print(channels_video_ids_dict)

    # Get the videos meta data
    #videos_meta_data = ModVIDEOmetaDATA.get_videos_meta_data_for_channels(pre_def_channel_ids, api_connection)
    #print(videos_meta_data)

    all_channels_all_video_data_dict= {}
    print(all_channels_all_video_data_dict)
    for video_ids in channels_video_ids_dict.values():
        video_meta_data_dict = ModVIDEOmetaDATA.get_videos_meta_data_for_channels(video_ids, api_connection)
        all_channels_all_video_data_dict.update(video_meta_data_dict)

    # Get the comments meta data for the videos
    all_videos_all_comments_dict = {}
    print(all_videos_all_comments_dict)

    for video_ids in channels_video_ids_dict.values():
        videos_comment_meta_data_dict = ModVIDEOmetaDATA.get_comments_meta_data_for_video_ids(video_ids, api_connection)
        all_videos_all_comments_dict.update(videos_comment_meta_data_dict)

    # Save the fetched values to the database
    db_int.add_data_to_channel_dets_table(all_channels_all_video_data_dict, db_conn)

    # save the fetched video details values to the database
    db_int.add_data_to_video_dets_table()
    # Start and call stream list interface -

    """# Fetch the saved channels data, to show existing data in streamlit
    channels_info = db_int.fetch_all_channel_details(db_conn)"""

    # Use this channels_info to show in stream lit

    """# Here or directly in the module, let us say the user enters a channel id, the following steps should help
    channel_id_entered_by_user 

    # check if channel id already fetched and saved in db
    channel_details = db_int.fetch_channel_detail(channel_id_entered_by_user)

    if channel_details is None:
        channel_info = channel_details_fetcher.get_channel_info(channel_id_entered_by_user, api_connection)
        videos_meta_data = video_meta_data_fetcher.get_videos_meta_data_for_channel(channel_id_entered_by_user,
                                                                                    api_connection)

        video_ids = channel_details_fetcher.get_channel_playlist_video_ids(channel_id_entered_by_user, api_connection)
        videos_comment_meta_data_dict = video_meta_data_fetcher.get_comments_meta_data_for_video_ids(
            channel_id_entered_by_user, api_connection)

        # Save these to the database

    else:
"""

# Print to stream lit that information about the channel is already present


def get_youtube_api_conn(api_key):
    """
    Function to get the YouTube API connection.

    Parameters:
    ----------
    api_key: str
        The API key needed to get the  YouTube API connection object

    Returns:
    -------
    The API connection object
    """
    api_service_name = "youtube"  # service name
    api_version = "v3"

    api_connection = build(api_service_name, api_version, developerKey = api_key)

    return api_connection


if __name__ == '__main__':
    #api_key = [sys.argv[0]]  # Check with 1 if 0 doesnt work
    api_key = "AIzaSyD_GoAklQv0-JaNW4HVOzJlScGhZPjUtoU"

    pre_def_channel_ids = ["UChGd9JY4yMegY6PxqpBjpRA", "UCrgLTEHTvedDsxdQzSAFyDA",
                           "UC5B0fGVovcbBJXQBx5kmRhQ", "UCKmE9i2iW0KaqgSxVFYmZUw", "UC21vCCoVSqgB7NzZjxB9weg",
                           "UC4c3Q2ym_hYei2cipr_KNaw", "UCy1lBBbXhtfzugF_LK2b6Yw",
                           "UCqwLyQUYPBP_4CVh7AMxNOQ", "UC7cgHgo42oYABKWabReHZyA"]
    ###"UC5HdAapbvqWN65GIqpWWL3Q",

    run(api_key, pre_def_channel_ids)
