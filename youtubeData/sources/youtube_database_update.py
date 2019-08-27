# Update the data of YouTube videos in the database

# When updating, the data of all the topics will be updated.
# The data updating will replace all the previous data.


from sources import database_common
from sources import dict_tools
from sources import youtube_concurrent_search
from __init__ import shared_mongodb_client


def update_youtube_videos_in_db(params):
    each_topic_videos_max_count = dict_tools.dict_get_nonnull(params, "each_max_count", default=50)

    db_topics = database_common.get_db_topics()
    db_topics_count = len(db_topics)

    mongodb_client = shared_mongodb_client
    db = mongodb_client["yousights"]

    # update each database topic

    i = 0
    while i < db_topics_count:
        this_db_topic = db_topics[i]

        this_params = {
            "query": this_db_topic["real_time_query"],
            "order": "relevance",
            "results_max_count": each_topic_videos_max_count,
            "want_descriptions": True,
            "want_en_transcripts": True,
            "want_comments": True,
        }

        this_topic_new_data = youtube_concurrent_search.search_youtube_videos_concurrently(this_params)

        # convert the format
        this_topic_new_items = this_topic_new_data["video_results"]
        items_count = len(this_topic_new_items)
        this_topic_new_db_items = []
        j = 0
        while j < items_count:
            this_item = this_topic_new_items[j]
            this_item_data = this_item["data"]
            this_db_item = {
                "item_index": j,
                "video_id": this_item["video_id"],
                "all_matcher": "a",
                "data_title": this_item_data["title"],
                "data_likeCount": this_item_data["likeCount"],
                "data_dislikeCount": this_item_data["dislikeCount"],
                "data_viewCount": this_item_data["viewCount"],
                "data_description": this_item_data["description"],
                "data_en_transcript": this_item_data["en_transcript"],
                "data_some_comments": this_item_data["some_comments"],
            }
            this_topic_new_db_items.append(this_db_item)
            j = j + 1

        # get the database collection object for this topic
        this_name_in_db = this_db_topic["name_in_db"]
        this_db_collection_name = "topicVideosOriginal_" + this_name_in_db
        this_db_collection = db[this_db_collection_name]

        # delete all videos of this topic
        this_db_collection.delete_many({"all_matcher": "a"})

        # add all new videos for this topic
        if len(this_topic_new_db_items) >= 1:
            this_db_collection.insert_many(this_topic_new_db_items)

        i = i + 1

    ret_info = {"result": "success"}

    return ret_info
