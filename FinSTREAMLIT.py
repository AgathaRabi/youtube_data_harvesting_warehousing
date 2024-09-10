from googleapiclient.discovery import build
import streamlit as st
import psycopg2
import pandas as pd
import FinDATABASEinterface as db_int
from sqlalchemy import create_engine
import plotly.express as px
import FinMAIN
import FinVIDEOmetaDATA
import FinChannelDETAILS

# Get the local DB connection
db_conn = db_int.get_local_db_conn()
api_key = "AIzaSyD_GoAklQv0-JaNW4HVOzJlScGhZPjUtoU"
API_conn = FinMAIN.get_youtube_api_conn(api_key)

# The streamlit program lines
# st.set_page_config(layout="wide")
st.title(":red[YOUTUBE DATA HARVESTING AND WAREHOUSING]"
         "📚💻✍🏼📓📶")
st.sidebar.title("VIEW")
page = st.sidebar.radio("click on", ["🏡Home", "🖨️Channel Data", "📞I/p Channel Id", "📜Queries & Answers", "🦾 Outcomes"])

if page == "🏡Home":

    st.markdown(
        f"""
            <style>
            .stApp {{
                background-image: url("https://cdn.pixabay.com/animation/2023/03/30/23/59/23-59-32-75_512.gif");
                background-repeat: no-repeat;
                background-size: 400px 300px;
                background-position: center bottom;
                             
            }}
            </style>
            """,
        unsafe_allow_html=True
    )
    st.markdown('''
    ## :rainbow[A Brief About the Project] 
    ### :blue[This project aims to get data analytics of multiple youtube channels, through API, persist to SQL database and visualize, the basic analytics through Streamlit.]    
    ''', True)


elif page == "🖨️Channel Data":
    
    st.markdown(
        f"""
                <style>
                .stApp {{
                    background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRufljZ-pTjwXA72dV1jA6w_daa2vvpOIYowA&s");
                    background-size: cover;

                }}
                </style>
                """,
        unsafe_allow_html=True
    )
    show_tables_list = st.radio("SELECT THE TABLE FOR VIEW",
                                ("CHANNEL DETAILS", "VIDEO DETAILS", "COMMENT DETAILS"))

    ## appropriate show table functions to be called for the choice made:
    if show_tables_list == "CHANNEL DETAILS":

        SQL_query = pd.read_sql('''SELECT * FROM channels''', db_conn)
        df_ch_details = st.dataframe(SQL_query)

        SQL_query_chart = pd.read_sql('''SELECT channel_name, subscribers_count, 
                                    views_channel, total_videos FROM channels''',
                                      db_conn)
        df_chart = pd.DataFrame(SQL_query_chart, columns = ["channel_name", "subscribers_count", "total_videos"])
        # st.bar_chart(df_chart, x = ["subscribers_count"], y = ["channel_name"])
        chart_subscriber_count = px.bar(df_chart, y = "subscribers_count", x = "channel_name",
                                      text_auto = '.2s', title = "Subscriber Count for Each Channel")
        st.plotly_chart(chart_subscriber_count, use_container_width=True)
        chart_total_videos = px.bar(df_chart, y = "total_videos", x = "channel_name",
                                      text_auto = '.2s', title = "Videos in Each Channel", color = 'total_videos')
        st.plotly_chart(chart_total_videos, use_container_width=True)

    elif show_tables_list == "VIDEO DETAILS":
        SQL_query = pd.read_sql('''SELECT * FROM video_details''', db_conn)
        df_video_details = st.dataframe(SQL_query)
        SQL_query_chart = pd.read_sql('''SELECT channel_name, number_views, 
                                        number_likes FROM video_details''', db_conn)
        df_chart = pd.DataFrame(SQL_query_chart, columns=["channel_name", "number_views", "number_likes"])
        chart_views_count = px.bar(df_chart, y="number_views", x="channel_name",text_auto='.2s',
                                   title="Total views of all videos for Each Channel")
        st.plotly_chart(chart_views_count, use_container_width=True)
        chart_likes_count = px.bar(df_chart, y="number_likes", x="channel_name",text_auto='.2s',
                                   title="All likes for all videos for Each Channel", color='number_likes')
        st.plotly_chart(chart_likes_count, use_container_width=True)

    elif show_tables_list == "COMMENT DETAILS":
        SQL_query = pd.read_sql('''SELECT * FROM comment_details''', db_conn)
        df_video_details = st.dataframe(SQL_query)


elif page == "📞I/p Channel Id":
    st.markdown(
        f"""
                           <style>
                           .stApp {{
                               background-image: url("https://classandtrashshow.wordpress.com/wp-content/uploads/2014/06/minions1.gif");
                               background-repeat: no-repeat;
                               background-size: 600px 500px;
                               background-position: center bottom;

                           }}
                           </style>
                           """,
        unsafe_allow_html=True
    )
    channel_id_streamlit = st.text_input("Enter the Channel ID 👇")
    if st.button("collect and store data 🗂️"):
        channel_details = db_int.fetch_channel_detail(channel_id_streamlit, db_conn)

        if channel_details is None:
            channel_info = FinChannelDETAILS.get_channel_info(channel_id_streamlit, API_conn)
            video_ids = FinChannelDETAILS.get_channel_playlist_video_ids(channel_id_streamlit, API_conn)
            video_meta_data = FinVIDEOmetaDATA.get_videos_meta_data_for_videos(video_ids, API_conn)
            video_comment_meta_data = FinVIDEOmetaDATA.get_comment_details_videos(
                                                                        video_ids, API_conn)
            #print(channel_info)
            #print(pd.DataFrame(channel_info, index = [0]))
            db_int.add_data_to_channel_dets_table(pd.DataFrame(channel_info, index = [0]), db_conn)
            db_int.add_data_to_video_dets_table(pd.DataFrame(video_meta_data), db_conn)
            db_int.add_data_to_comments_dets_table(pd.DataFrame(video_comment_meta_data), db_conn)



        else:
            st.write("The channel id is already present")

elif page == "📜Queries & Answers":

    st.markdown(
        f"""
                    <style>
                    .stApp {{
                        background-image: url("https://media.dev.to/cdn-cgi/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fscsioqdh89dvnbvk7rm9.gif");
                        background-repeat: no-repeat;
                        background-size: 400px 300px;
                        background-position: right top;
                        
                    }}
                    </style>
                    """,
        unsafe_allow_html=True
    )

    my_data_base = psycopg2.connect(host="localhost",
                                    user="postgres",
                                    password="phoenix275",
                                    database="youtube_data",
                                    port="5432")
    row_pointer_cursor = my_data_base.cursor()

    question = st.selectbox("Select your Question", ("1. List of all the videos and the Channel name",  ## shortening the questions for the select tab
                                                    "2. Channels with the most number of videos",
                                                    "3. top 10 most viewed videos and their respective channels",
                                                    "4. No. of comments in each video and corresponding video name",
                                                    "5. Videos with highest no. of likes and corresponding video name",
                                                    "6. Likes of all videos and the video names",
                                                    "7. Total  views of each channel and channel name",
                                                    "8. Videos published in the year of 2024 and channel name",
                                                    "9. average duration of videos in each channel and channel name",
                                                    "10. videos with the highest number of comments and channel name"))

    ## query one - retrieving the ans from sql and displaying in streamlit

    if question == "1. List of all the videos and the Channel name":

        query_one = pd.read_sql('''SELECT video_title , 
                                channel_name FROM video_details''', db_conn)
        dataframe_ans_q1 = st.dataframe(query_one)


    elif question == "2. Channels with the most number of videos":

        query_two = pd.read_sql('''SELECT channel_name , total_videos FROM channels
                    order by total_videos desc''', db_conn)
        dataframe_ans_q2 = st.dataframe(query_two)
        query_two_chart = pd.read_sql('''SELECT channel_name, total_videos FROM channels''',
                                      db_conn)
        df_chart = pd.DataFrame(query_two_chart, columns=["channel_name", "total_videos"])
        chart_total_videos = px.bar(df_chart, y="total_videos", x="channel_name",
                                    color_discrete_sequence = ['#992193'] * len(df_chart),
                                    text_auto='.2s', title="No. of Videos for Each Channel")
        chart_total_videos.update_layout(title_font_color='blue', title_font=dict(size=24))
        st.plotly_chart(chart_total_videos, use_container_width=True)


    elif question == "3. top 10 most viewed videos and their respective channels":

        query_three = pd.read_sql('''SELECT number_views , channel_name ,
                        video_title FROM video_details 
                        where number_views is not null order by number_views desc limit 10''', db_conn)
        dataframe_ans_q3 = st.dataframe(query_three)
        query_three_chart = pd.read_sql('''SELECT number_views , channel_name ,
                                        video_title FROM video_details 
                                        where number_views is not null''', db_conn)
        df_chart = pd.DataFrame(query_three_chart, columns=["number_views", "video_title", "channel_name"])
        chart_total_views = px.bar(df_chart, y="number_views", x="channel_name",
                                    color_discrete_sequence=['maroon'] * len(df_chart),
                                    text_auto='.2s', title="No. of Likes in Each Channel")
        chart_total_views.update_layout(title_font_color='dark green', title_font=dict(size=24))
        st.plotly_chart(chart_total_views, use_container_width=True)
        piechart_total_views = px.pie(df_chart, values='number_views', names='channel_name')
        st.plotly_chart(piechart_total_views, theme=None)

    elif question == "4. No. of comments in each video and corresponding video name":

        query_four = pd.read_sql('''select number_comments , video_title from video_details 
                                        where number_comments is not null''', db_conn)
        dataframe_ans_q4 = st.dataframe(query_four)


    elif question == "5. Videos with highest no. of likes and corresponding video name":

        query_five = pd.read_sql('''SELECT channel_name, number_likes, 
                                video_title FROM video_details WHERE number_likes is not null
                                order by number_likes desc''', db_conn)
        dataframe_ans_q5 = st.dataframe(query_five)
        query_five_chart = pd.read_sql('''SELECT channel_name, number_likes, video_title FROM video_details 
                                        where number_likes is not null''', db_conn)
        df_chart = pd.DataFrame(query_five_chart, columns=["number_likes", "video_title", "channel_name"])
        chart_total_views = px.bar(df_chart, y="number_likes", x="channel_name",
                                   color_discrete_sequence=['#219099'] * len(df_chart),
                                   text_auto='.2s', title="No. of Likes in Each Channel")
        chart_total_views.update_layout(title_font_color = '#2F1264', title_font=dict(size=24))
        st.plotly_chart(chart_total_views, use_container_width=True)
        piechart_total_views = px.pie(df_chart, values='number_likes', names='channel_name')
        st.plotly_chart(piechart_total_views, theme=None)

    elif question == "6. Likes of all videos and the video names":

        query_six = pd.read_sql('''select number_likes, 
                            video_title from video_details where number_likes is not null''', db_conn)
        dataframe_ans_q6 = st.dataframe(query_six)


    elif question == "7. Total  views of each channel and channel name":

        query_seven = pd.read_sql('''select channel_name as name_of_channel, 
                        views_channel as total_views_channel from channels''', db_conn)
        dataframe_ans_q7 = st.dataframe(query_seven)



    elif question == "8. Videos published in the year of 2024 and channel name":

        query_eight = pd.read_sql('''select video_title, published_date, 
                                    channel_name from video_details
                                    where extract(year from published_date) = '2024' ''', db_conn)
        dataframe_ans_q8 = st.dataframe(query_eight)



    elif question == "9. average duration of videos in each channel and channel name":

        query_nine = pd.read_sql('''SELECT channel_name, 
                                AVG(duration_video) as average_duration
                                FROM video_details group by channel_name''', db_conn)
        dataframe_ans_q9 = st.dataframe(query_nine)
        query_nine_chart = pd.read_sql('''SELECT channel_name, 
                                AVG(duration_video) as average_duration
                                FROM video_details group by channel_name''', db_conn)
        df_chart = pd.DataFrame(query_nine_chart, columns=["average_duration", "channel_name"])
        chart_video_avg_duration = px.bar(df_chart, y="average_duration", x="channel_name",
                                   color_discrete_sequence=['#219099'] * len(df_chart),
                                   text_auto='.2s', title="Average duration of videos in Each Channel")
        chart_video_avg_duration.update_layout(title_font_color='#2F1264', title_font=dict(size=24))
        st.plotly_chart(chart_video_avg_duration, use_container_width=True)
        piechart_total_views = px.pie(df_chart, values='average_duration', names='channel_name')
        st.plotly_chart(piechart_total_views, theme=None)

    elif question == "10. videos with the highest number of comments and channel name":

        query_ten = pd.read_sql('''select video_title, number_comments, 
                            channel_name from video_details 
                            where number_comments is not null order by number_comments desc''', db_conn)
        dataframe_ans_q10 = st.dataframe(query_ten)

elif page == "🦾 Outcomes":
    st.markdown(
        f"""
                        <style>
                        .stApp {{
                            background-image: url("https://miro.medium.com/v2/resize:fit:1000/1*2XVKVxYQYIjuAEmc7kO0YQ.gif");
                            background-repeat: no-repeat;
                            background-size: 350px 250px;
                            background-position: bottom right;

                        }}
                        </style>
                        """,
        unsafe_allow_html=True
    )
    st.write("On completion of this capstone project, the following are my takeaways:")
    st.write("1. Able to write code to fetch data from YouTube using Google API")
    st.write("2. learnt to stored the fetched data into SQL as Data Base")
    st.write("3. have been able to visualize the data using STREAMLIT UI")
    st.write("4. have been able to collect data for up to 10 different YouTube channels")
    st.write("5. Am more confident about debugging")


# dark pink - url("https://i.pinimg.com/originals/5f/19/79/5f197938702983ec7b9e3ad700f1f7cc.gif");
# simple utube - url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5DSnAllpbDrfsNbsMMEV9LhUQWDc0Czg40Q&s");
# paper design and scissors - url("https://i.pinimg.com/originals/5f/19/79/5f197938702983ec7b9e3ad700f1f7cc.gif");