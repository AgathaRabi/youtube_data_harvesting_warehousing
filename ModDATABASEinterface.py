"""
Module with functions to perform Create, Read, Update, Delete operations on the database
"""

import psycopg2


def get_local_db_conn():
    """
    Function to connect to the local database and return
    the connection object.

    Retuns:
    ------
    Database connectionn object
    """
    my_data_base_conn = psycopg2.connect(host="localhost",
                                         user="postgres",
                                         password="phoenix275",
                                         database="youtube_data",
                                         port="5432")
    my_data_base_conn.autocommit = True
    return my_data_base_conn


def drop_and_create_channel_dets_table(db_conn):
    """
    Function to drop the current channel table, if it exists
    and create a new empty table.

    Parameters:
    ----------
    db_conn:
        The database connection object
    """

    cursor = db_conn.cursor()

    drop_query = '''drop table if exists channels'''
    cursor.execute(drop_query)

    try:
        create_query = '''create table if not exists channels(Channel_Name varchar(100),
                                                               Channel_Id varchar(80) primary key,
                                                                Subscribers_Count bigint,
                                                                Views_Channel bigint,
                                                                Total_Videos int,
                                                                Channel_Description text,
                                                                Playlist_Id varchar(80))'''
        cursor.execute(create_query)

        # If auto-commit is true, is the below line needed? Can you check?
        db_conn.commit()

    except:
        print("Error in creating channels table!")


def drop_and_create_video_dets_table(db_conn):
    """
    Function to drop the current video details table, if it exists
    and create a new empty table.

    Parameters:
    ----------
    db_conn:
        The database connection object
    """

    cursor = db_conn.cursor()

    drop_query = '''drop table if exists video_details'''
    cursor.execute(drop_query)

    try:
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
        cursor.execute(create_query)

    except:
        print("Error in creating channels table!")


def drop_and_create_comment_dets_table(db_conn):
    """
    Function to drop the current comment details table, if it exists
    and create a new empty table.

    Parameters:
    ----------
    db_conn:
        The database connection object
    """

    cursor = db_conn.cursor()

    drop_query = '''drop table if exists comment_details'''
    cursor.execute(drop_query)

    try:
        create_query = '''create table if not exists comment_details(Comment_Gvn_Id varchar(100) primary key,
                                                                Video_Id varchar(100),
                                                                Comment_Text text,
                                                                Comment_Author varchar(150),
                                                                Comment_Published_Date timestamp)'''
        cursor.execute(create_query)

    except:
        print("Error in creating channels table!")


def add_data_to_channel_dets_table(channel_details, db_conn):
    """
    Function to add/ insert  channel details as a new row of data to
    the channel details table.

    Parameters:
    ----------
    channel_details:
        Pandas DataFrame object of the channel details
    """

    cursor = db_conn.cursor()

    for index, row in channel_details.iterrows():
        insert_into_sql = '''insert into channels (Channel_Name,
                                                    Channel_Id,
                                                    Subscribers_Count,
                                                    Views_Channel,
                                                    Total_Videos,
                                                    Channel_Description,
                                                    Playlist_Id) VALUES(%s, %s, %s, %s, %s, %s, %s);'''
        value_ch = (row['Channel_Name'],
                    row['Channel_Id'],
                    row['Subscribers_Count'],
                    row['Views_Channel'],
                    row['Total_Videos'],
                    row['Channel_Description'],
                    row['Playlist_Id'])

        cursor.execute(insert_into_sql, value_ch)

        db_conn.commit()


def add_data_to_video_dets_table(video_details, db_conn):
    """
        Function to add  video details as a new row of data to
        the video details table.

        Parameters:
        ----------
        video_details:
            Pandas DataFrame object of the video details
        """
    cursor = db_conn.cursor()

    for index, row in video_details.iterrows():
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

        cursor.execute(insert_query_vds, value_videoDetails)

    #row_pointer_cursor.execute(insert_query_vds, calling_videoData_values)
    db_conn.commit()


def add_data_to_comments_dets_table(comments_details, db_conn):
    """
        Function to add  comment details as a new row of data to
        the comments details table.

        Parameters:
        ----------
        comments_details:
            Pandas DataFrame object of the comments details
        """
    cursor = db_conn.cursor()

    for index, row in comments_details.iterrows():
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

        cursor.execute(insert_query_commentdts, value_commentdts)

    # row_pointer_cursor.execute(insert_query_vds, calling_videoData_values)
    db_conn.commit()


def fetch_channel_detail(channel_id, db_conn):
    """
    Function to fetch the channel details for a given channel.

    Parameters:
    ----------
    channel_id: str
        The id of the channel as a string
    db_conn:
        The database connection object

    Returns:
    -------
    The channel details. None if not found.
    """

    cursor = db_conn.cursor()

    # Not sure whether this is the correct syntax. have to check
    fetch_query = '''SELECT * FROM channels where Channel_Id=%s'''

    cursor.execte(fetch_query, channel_id)

    # Return object or None if result is empty.


def fetch_all_channel_details(db_conn):
    """
    Function to fetch all channel details data currently in the table
    """

    cursor = db_conn.cursor()

    # Not sure wether this is the correct syntax. have to check
    fetch_query = '''SELECT * FROM channels'''

    cursor.execte(fetch_query)

    # Return list of objects or None if result is empty.


