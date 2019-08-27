from requests.auth import _basic_auth_str
from __init__ import app
import server as analyticsAI_server  # NOQA

import unittest
import json


class TestAnalytics(unittest.TestCase):
    def setUp(self) -> None:
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        self.app_client = app.test_client()

    def test_analyticsai_from_db(self):
        query = {"params": {"query": "Python", "results_max_count": 5, "source": "cached"}}
        response = self.get_result_from_analyticsai(query)

        # Parse data from response
        response_data = json.loads(response.get_data(as_text=True))
        # check response from server with expected data
        self.assertEqual(response.status_code, 200)

        # check response has the expected number of videos
        self.assertEqual(response_data["video_count"], 5)

    """
    HELPER FUNCTIONS
    """

    def get_result_from_analyticsai(self, query):
        return self.app_client.post("/api/v1.0/data_analysis", data=json.dumps(query), headers={"Authorization": _basic_auth_str("xxxxxx", "xxxxxx"), "Content-Type": "application/json"})


if __name__ == "__main__":
    unittest.main()
