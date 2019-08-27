from sources import youtube_basic
from sources import dict_tools
import threading
from youtube_transcript_api import YouTubeTranscriptApi


def thread_get_video_basic_info(params):
    video_id = params[0]
    want_description = params[1]
    out_video_data = params[2]
    out_is_good = params[3]
    video_out_semaphore = params[4]
    finish_notify_semaphore = params[5]

    is_success = True
    this_video_basic_info = {}

    try:
        this_video_basic_info = youtube_basic.youtube_video_get_basic_info(video_id)
    except Exception:
        is_success = False

    video_out_semaphore.acquire()
    if is_success is True:
        out_video_data["title"] = this_video_basic_info["title"]
        out_video_data["likeCount"] = this_video_basic_info["likeCount"]
        out_video_data["dislikeCount"] = this_video_basic_info["dislikeCount"]
        out_video_data["viewCount"] = this_video_basic_info["viewCount"]
        if want_description is True:
            out_video_data["description"] = this_video_basic_info["description"]
    else:
        out_is_good["is_good"] = False
    video_out_semaphore.release()

    finish_notify_semaphore.release()


def thread_get_video_en_transcript(params):
    video_id = params[0]
    out_video_data = params[1]
    out_is_good = params[2]
    video_out_semaphore = params[3]
    finish_notify_semaphore = params[4]

    is_success = True
    this_video_en_transcript = []

    try:
        this_video_en_transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    except Exception:
        is_success = False

    video_out_semaphore.acquire()
    if is_success is True:
        out_video_data["en_transcript"] = this_video_en_transcript
    else:
        out_is_good["is_good"] = False
    video_out_semaphore.release()

    finish_notify_semaphore.release()


def thread_get_video_comments(params):
    video_id = params[0]
    out_video_data = params[1]
    # out_is_good = params[2]
    video_out_semaphore = params[3]
    finish_notify_semaphore = params[4]

    this_video_some_comments = {}

    try:
        this_video_some_comments = youtube_basic.youtube_video_get_comments(video_id, max_results=100)
    except Exception:
        this_video_some_comments = youtube_basic.youtube_video_create_empty_comments()

    video_out_semaphore.acquire()
    out_video_data["some_comments"] = this_video_some_comments
    video_out_semaphore.release()

    finish_notify_semaphore.release()


def async_get_video_basic_info(video_id, want_description, out_video_data, out_is_good, video_out_semaphore, finish_notify_semaphore):
    params = [video_id, want_description, out_video_data, out_is_good, video_out_semaphore, finish_notify_semaphore]
    p = threading.Thread(target=thread_get_video_basic_info, args=(params,))
    p.start()


def async_get_video_en_transcript(video_id, out_video_data, out_is_good, video_out_semaphore, finish_notify_semaphore):
    params = [video_id, out_video_data, out_is_good, video_out_semaphore, finish_notify_semaphore]
    p = threading.Thread(target=thread_get_video_en_transcript, args=(params,))
    p.start()


def async_get_video_comments(video_id, out_video_data, out_is_good, video_out_semaphore, finish_notify_semaphore):
    params = [video_id, out_video_data, out_is_good, video_out_semaphore, finish_notify_semaphore]
    p = threading.Thread(target=thread_get_video_comments, args=(params,))
    p.start()


def search_youtube_videos_concurrently(params):

    # internal parameters
    # When is_limit_threads_count is false, threads_count_limit has no effect.
    is_limit_threads_count = False
    threads_count_limit = 100

    # input parameters
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

    # prepare for multithreading

    count = len(video_ids)

    results_list = []
    results_is_good = []
    i = 0
    while i < count:
        this_video_id = video_ids[i]

        this_video_info = {"data": {}, "video_id": this_video_id}

        this_video_is_good = {"is_good": True}

        results_list.append(this_video_info)
        results_is_good.append(this_video_is_good)
        i = i + 1

    total_tasks_count = count
    if want_en_transcripts is True:
        total_tasks_count = total_tasks_count + count
    if want_comments is True:
        total_tasks_count = total_tasks_count + count

    current_tasks_count = 0
    finished_tasks_count = 0

    video_out_semaphores_list = []
    i = 0
    while i < count:
        this_video_out_semaphore = threading.Semaphore(1)
        video_out_semaphores_list.append(this_video_out_semaphore)
        i = i + 1

    thread_finish_notify_semaphore = threading.Semaphore(0)

    # do multithreading

    i = 0
    while i < count:
        this_video_id = video_ids[i]

        # get the basic information for this video
        if is_limit_threads_count is True:
            if current_tasks_count == threads_count_limit:
                thread_finish_notify_semaphore.acquire()
                current_tasks_count = current_tasks_count - 1
                finished_tasks_count = finished_tasks_count + 1
        async_get_video_basic_info(this_video_id, want_descriptions, results_list[i]["data"], results_is_good[i], video_out_semaphores_list[i], thread_finish_notify_semaphore)
        current_tasks_count = current_tasks_count + 1

        if want_en_transcripts is True:
            # get the English transcript for this video
            if is_limit_threads_count is True:
                if current_tasks_count == threads_count_limit:
                    thread_finish_notify_semaphore.acquire()
                    current_tasks_count = current_tasks_count - 1
                    finished_tasks_count = finished_tasks_count + 1
            async_get_video_en_transcript(this_video_id, results_list[i]["data"], results_is_good[i], video_out_semaphores_list[i], thread_finish_notify_semaphore)
            current_tasks_count = current_tasks_count + 1

        if want_comments is True:
            # get some (at most 100) comments for this video
            if is_limit_threads_count is True:
                if current_tasks_count == threads_count_limit:
                    thread_finish_notify_semaphore.acquire()
                    current_tasks_count = current_tasks_count - 1
                    finished_tasks_count = finished_tasks_count + 1
            async_get_video_comments(this_video_id, results_list[i]["data"], results_is_good[i], video_out_semaphores_list[i], thread_finish_notify_semaphore)
            current_tasks_count = current_tasks_count + 1

        i = i + 1

    # wait all threads finish

    while finished_tasks_count < total_tasks_count:
        thread_finish_notify_semaphore.acquire()
        current_tasks_count = current_tasks_count - 1
        finished_tasks_count = finished_tasks_count + 1

    # organize the results, removing results that are not good

    ret_results_list = []
    i = 0
    while i < count:
        this_video_is_good = results_is_good[i]
        if this_video_is_good["is_good"] is True:
            this_video_info = results_list[i]
            ret_results_list.append(this_video_info)
        i = i + 1

    ret_results_info = {"video_results_count": len(ret_results_list), "video_results": ret_results_list}

    return ret_results_info
