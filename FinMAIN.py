"""
The main module of the program
"""

from googleapiclient.discovery import build
import FinVIDEOmetaDATA
import FinDATABASEinterface as db_int
import FinChannelDETAILS


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


def run(api_key, pre_def_channel_ids):
    """
    :param api_key:
    :param pre_def_channel_ids:
    :return: the specified Youtube channel's channel details
                                            video id's
                                            video details
                                            video's message details
    """

    # Get the API connection
    api_connection = get_youtube_api_conn(api_key)

    # Get the local DB connection
    db_conn = db_int.get_local_db_conn()

    # Drop and create fresh tables
    db_int.drop_and_create_channel_dets_table(db_conn)
    db_int.drop_and_create_video_dets_table(db_conn)
    db_int.drop_and_create_comment_dets_table(db_conn)

    # Get the channel details for the pre-defined list of channel ids
    channels_info = FinChannelDETAILS.get_channels_info(pre_def_channel_ids, api_connection)
    db_int.add_data_to_channel_dets_table(channels_info, db_conn)

    # Get the video and comment details for the pre-defined list of channel ids and insert into db:

    for each_channel_id in pre_def_channel_ids:
        video_ids_channel = FinChannelDETAILS.get_channel_playlist_video_ids(each_channel_id, api_connection)
        videos_info = FinVIDEOmetaDATA.get_videos_meta_data_for_videos(video_ids_channel, api_connection)
        db_int.add_data_to_video_dets_table(videos_info, db_conn)
        comment_meta_data = FinVIDEOmetaDATA.get_comment_details_videos(video_ids_channel, api_connection)
        db_int.add_data_to_comments_dets_table(comment_meta_data, db_conn)

    db_int.fetch_all_channel_details(db_conn)
    return


if __name__ == '__main__':

    api_key = "xxxxxx"

    pre_def_channel_ids = ["UChGd9JY4yMegY6PxqpBjpRA", "UCrgLTEHTvedDsxdQzSAFyDA",
                           "UC5B0fGVovcbBJXQBx5kmRhQ", "UCKmE9i2iW0KaqgSxVFYmZUw",
                           "UC21vCCoVSqgB7NzZjxB9weg", "UC4c3Q2ym_hYei2cipr_KNaw"]

    run(api_key, pre_def_channel_ids)









#, "UCy1lBBbXhtfzugF_LK2b6Yw",
#"UCqwLyQUYPBP_4CVh7AMxNOQ", "UC7cgHgo42oYABKWabReHZyA"]
###"UC5HdAapbvqWN65GIqpWWL3Q",












"""api_key = "AIzaSyD_GoAklQv0-JaNW4HVOzJlScGhZPjUtoU"

pre_def_channel_ids = ["UChGd9JY4yMegY6PxqpBjpRA", "UCrgLTEHTvedDsxdQzSAFyDA",
                       "UC5B0fGVovcbBJXQBx5kmRhQ", "UCKmE9i2iW0KaqgSxVFYmZUw",
                       "UC21vCCoVSqgB7NzZjxB9weg"]  # ,
# "UC4c3Q2ym_hYei2cipr_KNaw", "UCy1lBBbXhtfzugF_LK2b6Yw",
# "UCqwLyQUYPBP_4CVh7AMxNOQ", "UC7cgHgo42oYABKWabReHZyA"]
###"UC5HdAapbvqWN65GIqpWWL3Q","""