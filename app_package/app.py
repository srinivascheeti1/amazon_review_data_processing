"""
app module maintains the initiation of flask application and data ingestion and cleansing process

Author: Srinivas Rao Cheeti
email: srinivascheeti1@gmail.com
Date: Feb 2, 2019
"""

from flask import Flask, request, jsonify, render_template
from flask import abort
import logging


try:
    import app_worker
except Exception as e:
    from app_package import app_worker
    print(e)


class DataProcessor:
    def __init__(self, log_level):
        self.app_wkr = app_worker.AppWorker('large', log_level)


# Create a Flask WSGI application
flaskapp = Flask(__name__)

app_wkr = DataProcessor('INFO').app_wkr


def initiate_data_ingestion_process():
    """Data ingestion and cleansing is initiated.

    """
    global market_data
    market_data = app_wkr.get_pandas_dataframe()


@flaskapp.route('/', methods=['GET'])
def index_page():
    """Basic index page to say hello

    :return: Hello
    """
    logging.info("Index page route")
    return render_template('<html><body><h1>Hello</h1></body></html>')


@flaskapp.route('/v1/data/marketplace/<marketplace>/review/<review_id>', methods=['GET'])
def get_market_place_review_id_data(marketplace, review_id):
    """Gets market place review data for a specific markets (country) review_id.

    :param marketplace: This field is the country abbreviation.
    :param review_id: This field is the review id that is being looked on.
    :return:
    """
    logging.info("Getting marketplace - {:} review with id {:}".format(marketplace, review_id))
    authorized = app_wkr.validate_api_key(request.headers)
    if not authorized:
        return jsonify({"message": "Unauthorized"}), 401
    return app_wkr.get_market_place_review_id_data(market_data, marketplace, review_id)


@flaskapp.route('/v1/data/marketplace/<marketplace>', methods=['GET'])
def get_entire_data_for_a_market(marketplace):
    """This function is used to request entire data for a market place.

    :param marketplace: This field is the country abbreviation.
    :return: Returns a JSON response with all the columns data for the matching marketplace.
    """
    logging.info("Getting market place reviews data for - {:} with either a limit or without".format(marketplace))
    authorized = app_wkr.validate_api_key(request.headers)
    if not authorized:
        return jsonify({"message": "Unauthorized"}), 401
    limit = request.args.get('limit')
    return app_wkr.get_entire_data_for_a_market(market_data, marketplace, limit)


@flaskapp.route('/v1/data/marketplace/reviewcount', methods=['GET'])
def get_total_count_of_reviews():
    """ This function performs a check on count of the number of rows in the data object.

    :return: Count of the number of reviews in the data object.
    """
    logging.info("Getting count of number of rows")
    return jsonify({"count": str(market_data.shape[0])})


@flaskapp.route('/v1/data/marketplace/object/<obj>/keyword/<keyword>', methods=['GET'])
def get_object_data_based_on_its_value(obj, keyword):
    """

    :param The data object from the path parameters of the API call.
    :param keyword: The keyword to search from the query parameter of the API call.
    :return:
    """
    logging.info("Getting data where object is - {:} and value is - {:}".format(obj, keyword))
    authorized = app_wkr.validate_api_key(request.headers)
    if not authorized:
        return jsonify({"message": "Unauthorized"}), 401
    return app_wkr.get_object_data_with_keyword(market_data, obj, keyword)


@flaskapp.route('/v1/data/registeruser', methods=['POST'])
def register_user():
    """ Route for the registration API.

    :return: Return generated api key for the registration request
    """
    logging.info("Registering user")
    if not request.json or not 'username' in request.json:
        return jsonify(abort(400, {'message': 'please provide username'}))
    else:
        api_key, username = app_wkr.register_user(request.get_json())
        return jsonify({'x-api-key': api_key, 'username': username})


if __name__ == '__main__':
    log_level = 'INFO'
    print('######################################################################')
    print('About to start data ingestion')
    print('######################################################################')
    initiate_data_ingestion_process()
    flaskapp.run(debug=True, host='0.0.0.0') # Start a development server
