"""
Module with functions to fetch metadata of videos
"""
import pandas as pd

def get_videos_meta_data_for_videos(obt_video_ids, api_connection):
    video_meta_data_for_allVs = []
    for each_video_id in obt_video_ids:
        request_video_information_api = api_connection.videos().list(part = 'snippet, contentDetails, statistics',
                                                                     id = each_video_id)
        get_video_details = request_video_information_api.execute()

        for item in get_video_details["items"]:
            video_meta_data = dict(Channel_Name = item['snippet']['channelTitle'],
                                    Channel_Id = item['snippet']['channelId'],
                                    Video_Id = item['id'], Video_Title = item['snippet']['title'],
                                    Tags_Video=item['snippet']['tags'] if 'tags' in item['snippet'] else None,
                                    Number_Likes=item['statistics'].get('likeCount'),
                                    Thumbnails = item['snippet']['thumbnails']['default']['url'], # if 'thumbnails' in item['snippet'] else None,
                                    Description = item['snippet']['description'] if 'description' in item['snippet'] else None,
                                    Published_Date = item['snippet']['publishedAt'],
                                    Duration_Video = item['contentDetails'].get('duration'),
                                   Number_Views = item['statistics'].get('viewCount'),
                                   Number_Comments = item['statistics'].get('commentCount'),
                                   Favourite_Count = item['statistics'].get('favouriteCount'),
                                   Definition = item['contentDetails']['definition'],
                                   Caption_Status = item['contentDetails']['caption'])
                                    ## above --- :  getting the specific details using slicing
            # number_likes=item['snippet']['statistics']['viewCount']
            video_meta_data_for_allVs.append(video_meta_data)

    return pd.DataFrame(video_meta_data_for_allVs)

#### all comments  :

"""
def get_comment_details_videos(total_video_ids, api_connection): ## all comments
    comment_meta_data_list =[]
    try:
        get_next_page_token = None
        ## to get all video ids a while loop is used

        #now to get the video id, for each video at a time
        #print(total_video_ids)
        for every_video_id in total_video_ids:
            all_comments_details = []
            request_video_comment_api = api_connection.commentThreads().list(part = 'snippet',
                                                                        videoId = every_video_id, maxResults = 50,
                                                                        pageToken = get_next_page_token)
            #print('Type of response: ', type(request_video_comment_api.execute()))
            to_get_comment_details = request_video_comment_api.execute()
            #print(every_video_id)
            while True:
                if 'nextPageToken' in to_get_comment_details:
                    get_next_page_token = to_get_comment_details['nextPageToken']
                    if get_next_page_token is None:
                        break
                else: break
            all_comments_details.append(to_get_comment_details)
            #print(to_get_comment_details)
            for comment_detail in to_get_comment_details['items']:
                ## getting specific details using slicing
                comment_meta_data = dict(Comment_Gvn_Id = comment_detail['snippet']['topLevelComment']['id'],
                                         Video_Id = comment_detail['snippet']['topLevelComment']['snippet']['videoId'],
                                         Comment_Text = comment_detail['snippet']['topLevelComment']['snippet']['textDisplay'],
                                         Comment_Author = comment_detail['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                         Comment_Published_Date = comment_detail['snippet']['topLevelComment']['snippet']['publishedAt'])
                comment_meta_data_list.append(comment_meta_data)


    except:
        pass

    return pd.DataFrame(comment_meta_data_list)"""

### only 50 comments

def get_comment_details_videos(total_video_ids, api_connection):  ### only 50 comments
    comment_meta_data_list =[]
    try:
        for every_video_id in total_video_ids:
            request_video_comment_api =api_connection.commentThreads().list(part = 'snippet',
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


    except:
        pass

    return pd.DataFrame(comment_meta_data_list)