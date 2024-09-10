**PROJECT STATEMENT**

	To create a StreamLit application to access and analyze data from multiple YouTube channels.
	Fetch data using google API.
	Store data in SQL.
	Retrieve data from SQL database for analysis and visualization.


**PROJECT OVERVIEW**

![image](https://github.com/user-attachments/assets/06f92d9d-5339-42bf-9928-19ff9f5c9a90)


**PROJECT IMPLEMENTATION FLOW**

	Fetch Data
 	Store Data in Database
  	Retrieve for analysis and Visualization

**CHANNEL DETAILS:**

	get_channel_info (channel_id, api_connection):  Function to fetch channel information, given the id for the channel.
	get_channels_info(channel_ids, api_connection): same as above, but for multiple channels.
	get_channel_playlist_video_ids(channel_id, api_connection): Function to fetch the video ids of a given channel's playlist videos
	get_channels_playlist_video_ids(channel_ids, api_connection): same as above, but for multiple channels.

 
**VIDEO META DATA:**

	get_videos_meta_data_for_videos(obt_video_ids, api_connection):  Function to fetch Video information, given the ids for the videos.
	get_comment_details_videos(total_video_ids, api_connection): Function to fetch the comment details, given the id’s for the videos.


**DATABASE INTERFACE:**

	get_local_db_conn(): Function to connect to the local database and return the connection object.
	drop_and_create_channel_dets_table(db_conn): Function to drop the current channel table, if it exists and create a new empty table.
	drop_and_create_video_dets_table(db_conn): Function to drop the current video details table, if it existsand create a new empty table.
	drop_and_create_comment_dets_table(db_conn):  Function to drop the current comment details table, if it exists and create a new empty table.
	add_data_to_channel_dets_table(channel_details, db_conn): Function to add/ insert  channel details as a new row of data to the channel details table.
	 add_data_to_video_dets_table(video_details, db_conn): Function to add  video details as a new row of data to the video details table.
	add_data_to_comments_dets_table(comments_details, db_conn): Function to add  comment details as a new row of data to the comments details table

 ![image](https://github.com/user-attachments/assets/2670c7d2-33d4-4142-bab7-0531ad7679f2)

**MAIN MODULE:**

	get_youtube_api_conn(api_key): Function to get the YouTube API connection.
	run(api_key, pre_def_channel_ids): Function that fetches the data and stores it in SQL.

**STREAMLIT MODULE:**

	Data display as tables.
	Graphical visualization of data.
	Answers to SQL queries.














