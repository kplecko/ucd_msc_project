from sources import youtube_data_analysis_live, youtube_data_analysis_cached
from __init__ import shared_mongodb_client

import logging
import traceback
import datetime

# logging = logging.getLogger('root')
logging.getLogger(__name__)


def record_search(query, search_type, time):
    db = shared_mongodb_client["yousights"]
    db_collection = db["searchRecords"]
    # Normalize the search query
    query = query.lower().strip()
    record_document = {"query": query, "search_type": search_type, "time": time, "all_matcher": "a"}
    db_collection.insert_one(record_document)


def analyticsai(params):
    query = params["query"]
    source = params["source"]

    record_search(query, source, datetime.datetime.utcnow())

    if source == "live":
        try:
            logging.info("Starting live search")
            analysis_results = youtube_data_analysis_live.analyticsai_live(params)
            return analysis_results
        except Exception as error:
            logging.error((f"ERROR while searching in live:  => {error}"))
            logging.error(traceback.format_exc())
    elif source == "cached":
        try:
            logging.info("Starting Cache search")
            analysis_results = youtube_data_analysis_cached.analyticsai_cached(params)
            return analysis_results
        except Exception as error:
            logging.error((f"ERROR while searching in cached:  => {error}"))
            logging.error(traceback.format_exc())
