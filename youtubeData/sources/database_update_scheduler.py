import threading
import datetime
import time
from __init__ import shared_mongodb_client
from sources import youtube_database_update


def perform_database_update():
    try:
        data_update_result = "unknown"

        start_moment = datetime.datetime.utcnow()
        try:
            update_params = {"each_max_count": 50}
            data_update_ret = youtube_database_update.update_youtube_videos_in_db(update_params)
            if data_update_ret["result"] == "success":
                data_update_result = "success"
        except Exception:
            data_update_result = "error"
        end_moment = datetime.datetime.utcnow()

        update_record = {
            "type": "original_data_update",
            "start_time": start_moment,
            "end_time": end_moment,
            "data_update_result": data_update_result
        }

        db_client = shared_mongodb_client
        db = db_client["yousights"]
        db_collection = db["dataAutomaticUpdateRecords"]
        db_collection.insert_one(update_record)
    except Exception:
        pass


def database_update_scheduler_thread_main():
    # read the parameters from the database
    db_client = shared_mongodb_client
    db = db_client["yousights"]
    db_collection = db["configuration"]
    config_name = "original_data_automatic_update_schedule"
    config_document = db_collection.find_one({"name": config_name})
    initial_min_interval_seconds = config_document["initial_min_interval_seconds"]
    initial_day_time_seconds_in_utc = config_document["initial_day_time_seconds_in_utc"]
    subsequent_interval_seconds = config_document["subsequent_interval_seconds"]

    # if initial_min_interval_seconds > 0, sleep for it; otherwise, it is ignored
    if initial_min_interval_seconds > 0:
        time.sleep(initial_min_interval_seconds)

    # create a duration object describing one day, and a duration object describing the interval between two updates
    one_day_seconds = 3600 * 24
    duration_one_day = datetime.timedelta(seconds=one_day_seconds)
    duration_subsequent_interval = datetime.timedelta(seconds=subsequent_interval_seconds)

    # get the initial update moment
    current_moment = datetime.datetime.utcnow()
    current_day_beginning_moment = current_moment.replace(hour=0, minute=0, second=0, microsecond=0)
    initial_day_offset_duration = datetime.timedelta(seconds=initial_day_time_seconds_in_utc)
    initial_update_moment = current_day_beginning_moment + initial_day_offset_duration
    while initial_update_moment < current_moment:
        initial_update_moment = initial_update_moment + duration_one_day

    # do the initial update
    if current_moment < initial_update_moment:
        sleep_duration = initial_update_moment - current_moment
        sleep_seconds = sleep_duration.total_seconds()
        time.sleep(sleep_seconds)
    perform_database_update()

    # do the subsequent updates
    this_update_moment = initial_update_moment
    is_continue = True
    while is_continue is True:
        this_update_moment = this_update_moment + duration_subsequent_interval
        current_moment = datetime.datetime.utcnow()

        is_to_update = True
        if this_update_moment < current_moment:
            # if this_update_moment < current_moment, then this time of update will be skipped
            # if this happens, then it may mean that the parameter subsequent_interval_seconds is too small
            is_to_update = False

        if is_to_update is True:
            if current_moment < this_update_moment:
                sleep_duration = this_update_moment - current_moment
                sleep_seconds = sleep_duration.total_seconds()
                time.sleep(sleep_seconds)
            perform_database_update()


class DatabaseUpdateScheduler():
    def __init__(self):
        self.database_update_thread = threading.Thread(target=database_update_scheduler_thread_main, daemon=True)

    def start(self):
        self.database_update_thread.start()
