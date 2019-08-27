# initi script to load all configuration and set application parameters

from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
import logging
import logging.config
import yaml
import json
import os
import pymongo


def load_json_file(file_path):
    # load credentials
    with open(file_path) as fpath:
        data = json.load(fpath)
        return data


def create_mongodb_client():
    try:
        mongodb_client = pymongo.MongoClient("mongodb+srv://xxxxx")
        return mongodb_client
    except Exception as error:
        logging.error(f"Error while connecting to MongoDB: {error}")
        return False


# create the shared MongoDB client
shared_mongodb_client = create_mongodb_client()

# Entity parameters
entity_type = ["ORGANIZATION", "CONSUMER_GOOD", "WORK_OF_ART"]
entity_max_count = 5

# application_path = os.path.dirname(os.path.realpath(sys.argv[0]))
application_path = os.path.dirname(os.path.abspath(__file__))

# Create logs directory
if not os.path.exists(application_path + "/logs"):
    os.makedirs(application_path + "/logs")

with open(application_path + "/config/logging.yml", "r") as stream:
    try:
        log_conf = yaml.safe_load(stream)
        logging.config.dictConfig(log_conf)
    except Exception as error:
        logging.error(f"Error while loading configuration: {error}")

app_config_file_path = application_path + "/config/config.json"
app_config = load_json_file(app_config_file_path)

youtubeDataURL = "http://127.0.0.1:5000" + app_config["YoutubeDataAPI"]
BasicAuthCredentials = app_config["BasicAuthCredentials"]

# try to get cloud port to confirm if environment is cloud
isCloud = os.getenv("PORT")
if isCloud:
    youtubeDataURL = "https://youtubedata.eu-gb.mybluemix.net" + app_config["YoutubeDataAPI"]

app = Flask(__name__)
CORS(app)

api = Api(app, version="1.0", title="YouSights AI API", description="YouSights AI component")
api.namespaces.clear()  # clear default namespace
api = api.namespace("api/v1.0/", description="YouSights AI API")
