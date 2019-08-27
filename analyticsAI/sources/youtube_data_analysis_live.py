from sources.youtube_analysis_computing import analysis_computing
from call_search_api import CallSearchAPI


def analyticsai_live(params):
    query = params["query"]
    source = params["source"]
    if params["results_max_count"]:
        results_max_count = params["results_max_count"]
    else:
        results_max_count = 10

    search_params = {"query": query, "order": "relevance", "results_max_count": results_max_count,
                     "want_descriptions": True, "want_en_transcripts": True, "want_comments": True}

    # get live search youtube data
    live_youtubedata = CallSearchAPI(search_params)

    # compute nalytics results
    if live_youtubedata:
        analysis_results = analysis_computing(query, source, live_youtubedata)
        if analysis_results:
            return analysis_results

    return False
