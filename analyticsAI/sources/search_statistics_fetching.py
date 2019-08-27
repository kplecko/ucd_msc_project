# For fetching statistics of users' searches

from __init__ import shared_mongodb_client


def fetch_search_statistics(params):
    # prepare parameters
    user_search_type = params["user_search_type"]
    statistics_mode = params["statistics_mode"]
    if user_search_type == "any":
        db_filter = {"all_matcher": "a"}
    else:
        db_filter = {"search_type": user_search_type}

    # read all search records from the database
    records = []
    db = shared_mongodb_client["yousights"]
    db_collection = db["searchRecords"]
    documents = db_collection.find(db_filter)
    for document in documents:
        this_record = {"query": document["query"], "search_type": document["search_type"], "time": document["time"]}
        records.append(this_record)

    # generate the statistics dictionary
    statistics_dict = {}
    records_count = len(records)
    i = 0
    while i < records_count:
        this_record = records[i]
        this_query = this_record["query"]
        if statistics_mode == "smart":
            this_query = this_query.strip()
            this_query = this_query.lower()

        if this_query in statistics_dict:
            this_statistic = statistics_dict[this_query]
            this_statistic["count"] = this_statistic["count"] + 1
        else:
            this_statistic = {"count": 1}
            statistics_dict[this_query] = this_statistic

        i = i + 1

    # generate the statistics list
    searches_count = len(records)
    statistics_list = []
    for query in statistics_dict:
        this_dict_item = statistics_dict[query]
        this_count = this_dict_item["count"]
        this_ratio = this_count / searches_count
        this_list_item = {"query": query, "count": this_count, "ratio": this_ratio}
        statistics_list.append(this_list_item)

    # sort the list on the count from the most to the least
    count = len(statistics_list)
    i = 0
    while i < count:
        target_item_index = i
        target_item = statistics_list[target_item_index]

        j = i + 1
        while j < count:
            test_item = statistics_list[j]
            if test_item["count"] > target_item["count"]:
                target_item_index = j
                target_item = statistics_list[target_item_index]
            j = j + 1

        if target_item_index > i:
            swap_item = statistics_list[i]
            statistics_list[i] = statistics_list[target_item_index]
            statistics_list[target_item_index] = swap_item

        i = i + 1

    # return the information
    ret_info = {"total_count": searches_count, "statistics_per_query": statistics_list}
    return ret_info
