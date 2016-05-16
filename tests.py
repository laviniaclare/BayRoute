from model import Agency, Route, Trip, StopTime, Stop
from server import get_routes_by_id

import unittest
import routes

####### Tests go here #######


class IntegrationTest(unittest.TestCase):

    def test_load_options(self):
        result = self.client.get('/')
        self.assertIn("Show Routes!", result.data)

    def test_prepare_routes_for_display(self):
        pass

    def test_get_routes_by_id_one_route(self):
        result = get_routes_by_id("['CT_SHUTTLE']")
        expected_result = [{u'5660669': [[37.3103897344, -121.8827510483], [37.3291912336, -121.9019291905]], u'5660682': [[37.3291912336, -121.9019291905], [37.3103897344, -121.8827510483]]}]
        self.assertEqual(result, expected_result)


class ModelTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
