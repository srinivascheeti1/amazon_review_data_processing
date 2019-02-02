"""
test_suit module contains the test cases necessary for the docker up and ingestion of data process to be validated

Author: Srinivas Rao Cheeti
email: srinivascheeti1@gmail.com
Date: Feb 2, 2019
"""

import unittest
import requests
import json


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.host = 'http://0.0.0.0:5000'
        self.test_user_name = 'tom'

    def test_count_api(self):
        count_response = requests.get(self.host + '/v1/data/marketplace/reviewcount')
        self.assertEqual(count_response.status_code, 200)

    def test_unauthorized(self):
        review_response = requests.get(self.host + '/v1/data/marketplace/US/review/R1AXGS1W4YFXMX')
        self.assertEqual(review_response.status_code, 401)

    def test_register_user_and_other_apis(self):
        headers = {"Content-Type": "application/json"}
        registration_response = requests.post(self.host + '/v1/data/registeruser',
                                              data=json.dumps({"username": self.test_user_name}),  headers=headers)
        data = json.loads(registration_response.content.decode('utf8').replace("'", '"'))
        self.assertEqual(registration_response.status_code, 200)
        self.assertEqual(data['username'], self.test_user_name)

        headers = {"x-api-key": data['x-api-key']}
        review_limit_response = requests.get(self.host + '/v1/data/marketplace/US?limit=1', headers=headers)
        self.assertEqual(review_limit_response.status_code, 200)

        headers = {"x-api-key": data['x-api-key']+'xyz'}
        review_limit_response = requests.get(self.host + '/v1/data/marketplace/US?limit=1', headers=headers)
        self.assertEqual(review_limit_response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
