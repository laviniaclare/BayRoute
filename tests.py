from model import Agency, Route, Trip, StopTime, Stop

import unittest
import routes

####### Tests go here #######


class IntegrationTest(unittest.TestCase):
    """Tests for the routes.py file to make sure all routes work as they should"""

    def setUp(self):
        self.client = routes.app.test_client()
        routes.app.config['TESTING'] = True

    def test_load_options(self):
        result = self.client.get('/')
        self.assertIn("Show Routes!", result.data)

    def test_prepare_routes_for_display(self):
        pass

    def test_get_routes_by_id_one_route(self):
        result = routes.get_routes_by_id('["CT_SHUTTLE"]')
        expected_result = [{u'5660669': [
                                [37.3103897344, -121.8827510483],
                                [37.3291912336, -121.9019291905]
                                ],
                            u'5660682': [
                                [37.3291912336, -121.9019291905],
                                [37.3103897344, -121.8827510483]
                                ]
                            }]
        self.assertEqual(result, expected_result)

    def test_get_routes_by_id_multiple_routes(self):
        result = routes.get_routes_by_id('["GF_1", "SB_3", "YV_SHUTTLE"]')
        expected_result = [{u'5175881': [
                                [37.944027, -122.508869],
                                [37.795233, -122.39365]
                                ],
                            u'5175858': [
                                [37.795233, -122.39365],
                                [37.944027, -122.508869]
                                ]
                            }, {
                            u'5185915': [
                                [38.1011949057, -122.2630594806],
                                [37.7961455533, -122.3936224975],
                                [37.7961455533, -122.3936224975],
                                [37.8090739229, -122.4091265542],
                                [37.8090739229, -122.4091265542],
                                [38.1011957523, -122.2630568433]
                                ],
                            u'5185918': [
                                [38.1011949057, -122.2630594806],
                                [37.8090739229, -122.4091265542],
                                [37.8090739229, -122.4091265542],
                                [37.7961455533, -122.3936224975],
                                [37.7961455533, -122.3936224975],
                                [38.1011957523, -122.2630568433]
                                ]
                            }, {
                            u'3940844': [
                                [38.393729, -122.364376],
                                [38.4012149934, -122.3601657516],
                                [38.4036400505, -122.3619679799],
                                [38.407695064, -122.3677324599],
                                [38.403021, -122.362886],
                                [38.4012149934, -122.3601657516],
                                [38.398133, -122.358019]
                                ]
                            }]

        self.assertEqual(result, expected_result)


class ModelTest(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
