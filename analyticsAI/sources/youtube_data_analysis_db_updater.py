from sources.database_common import get_db_topics
from __init__ import shared_mongodb_client
from sources.youtube_analysis_computing import analysis_computing

import pymongo
import logging
import traceback


def db_update():
    try:
        updated_topics = get_db_topics()
    except Exception as error:
        logging.error(f"Error while db updater getting the topics object from the database: {error}")
        logging.error(traceback.format_exc())
    # Get database 'yousights'
    db = shared_mongodb_client["yousights"]

    for topic in updated_topics:
        original_videos = list()
        topic_name = topic["name"]
        topic_name_in_db = topic["name_in_db"]

        db_collection = db["topicVideosOriginal_" + topic_name_in_db]
        documents = db_collection.find(filter={"all_matcher": "a"}, sort=[("item_index", pymongo.ASCENDING)])
        for document in documents:
            video_data = {
                "title": document["data_title"],
                "likeCount": document["data_likeCount"],
                "dislikeCount": document["data_dislikeCount"],
                "viewCount": document["data_viewCount"],
                "description": document["data_description"],
                "en_transcript": document["data_en_transcript"],
                "some_comments": document["data_some_comments"],
            }
            original_videos.append({"video_id": document["video_id"], "data": video_data})

        all_videos_original = {"video_results_count": len(original_videos), "video_results": original_videos}

        # Analysis data computing, includes the similarity
        source = "cached"
        videos_analyzed_data = analysis_computing(topic_name, source, all_videos_original)

        video_statistic_data = videos_analyzed_data["video_statistic_data"]
        db_new_items = list()
        for index, analyzed_video in enumerate(video_statistic_data):
            this_original_video = original_videos[index]["data"]
            analyzed_video_data = analyzed_video["data"]
            this_new_item = {
                "item_index": index,
                "video_id": analyzed_video["video_id"],
                "all_matcher": "a",
                "original_data_title": this_original_video["title"],
                "original_data_likeCount": this_original_video["likeCount"],
                "original_data_dislikeCount": this_original_video["dislikeCount"],
                "original_data_viewCount": this_original_video["viewCount"],
                "original_data_description": this_original_video["description"],
                "original_data_en_transcript": this_original_video["en_transcript"],
                "original_data_some_comments": this_original_video["some_comments"],
                "analyzed_data_title": analyzed_video_data["title"],
                "analyzed_data_likeCount": analyzed_video_data["likeCount"],
                "analyzed_data_dislikeCount": analyzed_video_data["dislikeCount"],
                "analyzed_data_viewCount": analyzed_video_data["viewCount"],
                "analyzed_data_en_transcript": analyzed_video_data["en_transcript"],
                "analyzed_data_comments": analyzed_video_data["comments"],
            }
            db_new_items.append(this_new_item)

        db_collection = db["topicVideosAnalyzed_" + topic_name_in_db]
        # Delete collections
        db_collection.delete_many({"all_matcher": "a"})

        # Update collections
        if len(db_new_items) > 0:
            # Writing data into database
            db_collection.insert_many(db_new_items)

    return {"result": "success"}
