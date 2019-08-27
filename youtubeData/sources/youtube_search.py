# This Python module contains one function for searching YouTube videos and returning their information, including their English transcripts
# It uses both the official YouTube API and an unofficial YouTube transcript Python package


from sources import youtube_basic
from sources import dict_tools
from youtube_transcript_api import YouTubeTranscriptApi


def search_youtube_videos(params):

    query = params["query"]
    order = dict_tools.dict_get_existent(params, "order", None)
    max_results = dict_tools.dict_get_existent(params, "results_max_count", None)
    page_token = dict_tools.dict_get_existent(params, "page_token", None)
    want_descriptions = dict_tools.dict_get_existent(params, "want_descriptions", True)
    want_en_transcripts = dict_tools.dict_get_existent(params, "want_en_transcripts", True)
    want_comments = dict_tools.dict_get_existent(params, "want_comments", True)

    # You can enable page_token by simply removing the following line.
    page_token = None

    search_max_results = 5
    if max_results is not None:
        search_max_results = max_results

    basic_search_result = youtube_basic.youtube_video_basic_search(query, order=order, max_results=search_max_results, page_token=page_token)

    video_ids = basic_search_result["results_video_id"]

    count = len(video_ids)
    results_list = []
    i = 0
    while i < count:
        this_video_id = video_ids[i]
        this_video_isContinue = True

        # get basic information
        try:
            this_video_basic_info = youtube_basic.youtube_video_get_basic_info(this_video_id)
        except Exception:
            this_video_isContinue = False

        # get English transcript
        if (this_video_isContinue is True) and (want_en_transcripts is True):
            try:
                this_video_en_transcript = YouTubeTranscriptApi.get_transcript(this_video_id, languages=["en"])
            except Exception:
                this_video_isContinue = False

        # get comments
        if (this_video_isContinue is True) and (want_comments is True):
            try:
                this_video_comments = youtube_basic.youtube_video_get_comments(this_video_id, max_results=100)
            except Exception:
                this_video_comments = youtube_basic.youtube_video_create_empty_comments()

        # put them together
        if this_video_isContinue is True:
            this_video_data_dict = {
                "title": this_video_basic_info["title"],
                "likeCount": this_video_basic_info["likeCount"],
                "dislikeCount": this_video_basic_info["dislikeCount"],
                "viewCount": this_video_basic_info["viewCount"],
            }

            if want_descriptions is True:
                this_video_data_dict["description"] = this_video_basic_info["description"]

            if want_en_transcripts is True:
                this_video_data_dict["en_transcript"] = this_video_en_transcript

            if want_comments is True:
                this_video_data_dict["some_comments"] = this_video_comments

            this_video_dict = {"data": this_video_data_dict, "video_id": this_video_id}

            results_list.append(this_video_dict)

        i = i + 1

    # build the final return
    ret_dict = {"video_results_count": len(results_list), "video_results": results_list}
    # ret_dict["pageInfo"] = basic_search_result["pageInfo"]
    # ret_dict["nextPageToken"] = basic_search_result["nextPageToken"]
    # ret_dict["prevPageToken"] = basic_search_result["prevPageToken"]

    return ret_dict
