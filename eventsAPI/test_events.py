from requests.auth import _basic_auth_str
import unittest
import json
from __init__ import app
import server  # NOQA

app.testing = True


class TestEvents(unittest.TestCase):

    def test_main(self):
        query = {"keyword": "python", "lat": 53.3498, "lng": -6.2603}
        tester = app.test_client(self)
        result = tester.post('/api/v1.0/events', data=json.dumps(query),
                             headers={'Authorization': _basic_auth_str('xxxxxx', 'xxxxxxxx'),
                                      'Content-Type': 'application/json'})
        # check result from server with expected data
        self.assertEqual(
            result.status_code,
            200,
        )


TestEvents().test_main()
