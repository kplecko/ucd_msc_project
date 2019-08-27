#!/usr/bin/env python3
#
# UCD Abracadata - YouSights project Events microservice

# import python libs
import logging
from events import get_events
from flask import request, jsonify, abort
from flask_restplus import Resource
from flask_basicauth import BasicAuth
import os
from __init__ import app, api, application_path
from api_models import event_query_model, event_response_model
from version import __version__

logging.getLogger(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'xxxxxxxx'
app.config['BASIC_AUTH_PASSWORD'] = 'xxxxxxxx'

basic_auth = BasicAuth(app)
port = int(os.getenv('PORT', 5002))


# Events API
@api.route("/events")
class YouSightsEvents(Resource):
    @basic_auth.required
    @api.doc(description="Events API to get list of events from various sources including meetup and eventbrite")
    @api.expect(event_query_model)
    @api.marshal_with(event_response_model)
    def post(self):
        request_info = request.json
        search_topic = request_info["keyword"]
        search_lng = request_info["lng"]
        search_lat = request_info["lat"]
        events = get_events(search_topic, search_lat, search_lng)
        if events:
            return events
        else:
            abort(404, events)
        return jsonify(error="error while processing data")


@api.route("/status")
class Status(Resource):
    @api.doc(description="Events application status API")
    def get(self):
        # return app version
        return jsonify(application="Events", version=__version__)


@api.route("/logs")
class Logs(Resource):
    @basic_auth.required
    @api.doc(description="Events application logs")
    def get(self):
        file_path = application_path + "/logs/server.log"
        with open(file_path) as file:
            logs = file.readlines()

        return jsonify(application="Events", logs=logs)


# start server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
