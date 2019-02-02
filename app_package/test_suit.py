import unittest

try:
    import app
    import app_worker
except Exception as e:
    print(e)


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.flaskapp.test_client()
        self.app_wkr = app_worker.AppWorker('small', 'INFO')

    # def test_index(self):
    #     rv = self.app.get('/')
    #     assert rv.status == '200 OK'

    def test_review_count(self):
        rv = self.app.get('/v1/data/marketplace/object/review_id/keyword/R2BUV9QJI2A00X')
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv[0].customer_id, 7360347)
        print("@@@@@@@@@@@#################$$$$$$$$$$$@@@@@@@@@@@")

    #     rv = self.app.get('/add/0/10')
    #     self.assertEqual(rv.status, '200 OK')
    #     self.assertEqual(rv.data, '10')
    #
    def test_404(self):
        rv = self.app.get('/v1/data/marketplace/object/review_id/keyword/ABC')
        self.assertEqual(rv.status, '404 NOT FOUND')
        print("@@@@@@@@@@@#################$$$$$$$$$$$@@@@@@@@@@@")


if __name__ == '__main__':
    unittest.main()