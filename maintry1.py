"""
The main module of the program
"""
import pandas as pd
from googleapiclient.discovery import build
import ModCHANNELSdetails
import ModVIDEOmetaDATA
import ModDATABASEinterface as db_int



# Get the local DB connection
db_conn = db_int.get_local_db_conn()

# Drop and create fresh tables
db_int.drop_and_create_channel_dets_table(db_conn)
db_int.drop_and_create_video_dets_table(db_conn)
db_int.drop_and_create_comment_dets_table(db_conn)


pre_def_channel_ids = ["UChGd9JY4yMegY6PxqpBjpRA", "UCrgLTEHTvedDsxdQzSAFyDA",
                           "UC5B0fGVovcbBJXQBx5kmRhQ", "UCKmE9i2iW0KaqgSxVFYmZUw", "UC21vCCoVSqgB7NzZjxB9weg",
                           "UC4c3Q2ym_hYei2cipr_KNaw", "UCy1lBBbXhtfzugF_LK2b6Yw",
                           "UCqwLyQUYPBP_4CVh7AMxNOQ", "UC7cgHgo42oYABKWabReHZyA"]





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

api_key = "AIzaSyD_GoAklQv0-JaNW4HVOzJlScGhZPjUtoU"
# Get the API connection
api_connection = get_youtube_api_conn(api_key)



# Get the channel details for the pre defined list of channel ids
channels_info = ModCHANNELSdetails.get_channels_info(pre_def_channel_ids, api_connection)

db_int.add_data_to_channel_dets_table(channels_info, db_conn)

# Get the video ids for the channels playlist
channels_video_ids_list = ModCHANNELSdetails.get_channels_playlist_video_ids(pre_def_channel_ids,
                                                                             api_connection)

"""all_channels_all_video_data_dict = {}
#print(all_channels_all_video_data_dict)
for video_ids in channels_video_ids_dict.values():
    video_meta_data_dict = ModVIDEOmetaDATA.get_videos_meta_data_for_channels(video_ids, api_connection)
    all_channels_all_video_data_dict.update(video_meta_data_dict)
all_channels_all_video_data_dict_dataFrame = pd.DataFrame(all_channels_all_video_data_dict)
print(all_channels_all_video_data_dict_dataFrame)"""
#db_int.add_data_to_video_dets_table(all_channels_all_video_data_dict_dataFrame, db_conn)


"""all_channels_all_video_data_dict = {}
print(all_channels_all_video_data_dict)
for video_ids in channels_video_ids_dict.values():
    video_meta_data_dict = ModVIDEOmetaDATA.get_videos_meta_data_for_channels(video_ids, api_connection)
    all_channels_all_video_data_dict.update(video_meta_data_dict)
all_channels_all_video_data_dict_dataFrame = pd.DataFrame(tuple(all_channels_all_video_data_dict))
print(all_channels_all_video_data_dict_dataFrame)"""


all_channels_all_video_data_list = []
#print(all_channels_all_video_data_dict)
for video_ids in channels_video_ids_list:
    video_meta_data_list = ModVIDEOmetaDATA.get_videos_meta_data_for_channels(video_ids, api_connection)
    all_channels_all_video_data_list.append(video_meta_data_list)
all_channels_all_video_data_list_dataFrame = pd.DataFrame(tuple(all_channels_all_video_data_list))
#print(all_channels_all_video_data_list)

db_int.add_data_to_video_dets_table(all_channels_all_video_data_list, db_conn)