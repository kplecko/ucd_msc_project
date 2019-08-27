from sources.database_common import get_db_topics
from __init__ import shared_mongodb_client

import pymongo
import logging
import traceback


def db_search(params):
    query = params["query"]
    if params["results_max_count"]:
        results_max_count = params["results_max_count"]
    else:
        results_max_count = 10

    try:
        topics = get_db_topics()
    except Exception as error:
        logging.error(f"Error while cached search getting the topics from the database: {error}")
        logging.error(traceback.format_exc())

    topic_is_found = False

    for topic in topics:
        if query == topic["name"]:
            topic_name_in_db = topic["name_in_db"]
            topic_is_found = True
            break

    if topic_is_found:
        try:
            db = shared_mongodb_client["yousights"]
            db_collection = db["topicVideosAnalyzed_" + topic_name_in_db]
        except Exception as error:
            logging.error(f"Error while cached search connecting the database: {error}")
            logging.error(traceback.format_exc())
        index_min = 0
        index_max = results_max_count - 1
        filter_index_min = {"item_index": {"$gte": index_min}}
        filter_index_max = {"item_index": {"$lte": index_max}}
        filter_full = {"$and": [filter_index_min, filter_index_max]}
        documents = db_collection.find(filter=filter_full, sort=[("item_index", pymongo.ASCENDING)])
        videos = list()
        for document in documents:
            video_data = {
                "title": document["analyzed_data_title"],
                "likeCount": document["analyzed_data_likeCount"],
                "dislikeCount": document["analyzed_data_dislikeCount"],
                "viewCount": document["analyzed_data_viewCount"],
                "en_transcript": document["analyzed_data_en_transcript"],
                "comments": document["analyzed_data_comments"],
            }

            video = {"video_id": document["video_id"], "data": video_data}

            videos.append(video)
    else:
        videos = []

    ret_info = {"video_statistic_data": videos, "video_count": len(videos)}

    return ret_info
