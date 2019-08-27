# For database operations

from __init__ import shared_mongodb_client


# Get information about all the database topics
def get_db_topics():
    topics = []

    db = shared_mongodb_client["yousights"]
    db_collection = db["topics"]
    documents = db_collection.find({"all_matcher": "a"})
    for document in documents:
        this_name = document["name"]
        this_name_in_db = document["name_in_db"]
        this_real_time_query = document["real_time_query"]
        this_topic = {"name": this_name, "name_in_db": this_name_in_db, "real_time_query": this_real_time_query}
        topics.append(this_topic)

    return topics
