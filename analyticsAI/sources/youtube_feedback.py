from __init__ import shared_mongodb_client
import datetime


def feedback_record(params):
    feedback = params["feedback"]

    # Connecting the database
    db = shared_mongodb_client["yousights"]
    db_collection = db["feedbackRecords"]
    record_document = {"feedback": feedback, "time": datetime.datetime.utcnow(), "all_matcher": "a"}
    db_collection.insert_one(record_document)

    return {"message": "feedback record success"}
