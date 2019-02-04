"""
app_worker module is used to maintain business logic required for processing each of the request

Author: Srinivas Rao Cheeti
email: srinivascheeti1@gmail.com
Date: Feb 2, 2019
"""

from flask import abort, jsonify
import uuid
import dask.dataframe as dd
import pandas as pd
import requests
import io

try:
    import logging
    import app_dal
except Exception as e:
    from app_package import app_dal
    print(e)


class AppWorker:
    def __init__(self, file_size, level):
        """

        :param file_size: Initializes the filesize
        :param level: level of logging (DEBUG, INFO etc)
        """
        self.file_size = file_size
        self.logs = logging.basicConfig(level=level)
        self.dal = app_dal.AppDAL(level)

    def register_user(self, request):
        """ This function inserts the registered user details into mysql database(userbase table).

        :param request: JSON request content provided as part of registration API call.
        :return: Returns apikey (GUID) and the username
        """
        username = request.get('username')
        apikey = uuid.uuid4()
        connection = self.dal.get_sql_connection()
        cursor = connection.cursor(buffered=True)
        try:
            cursor.execute("""INSERT INTO userbase (apikey, username) VALUES (%s,%s)""", (str(apikey), username))
        except Exception as e:
            print("Logging error {:} which could be sent as a email or moved to a Queue service.".format(e))
            # abort(500, {'message': 'user could not be registered'})
            return self.make_error(500, 'user could not be registered')
        connection.commit()
        connection.close()
        cursor.close()
        return apikey, username

    def validate_api_key(self, headers):
        """ This function queries mysql userbase table to check if the user exist.

        :param headers: Header information for API call.
        :return: Boolean value set to check if the user is authenticated.
        """
        authorized = False
        auth_key = headers.get("x-api-key")
        connection = self.dal.get_sql_connection()
        cursor = connection.cursor(buffered=True)
        try:
            cursor.execute("SELECT * FROM userbase WHERE apikey = '{:}'".format(auth_key))
        except Exception as e:
            print("Logging error {:} which could be sent as a email or moved to a Queue service.".format(e))
            return self.make_error(500, 'apikey could not be generated')
            # abort(500, {'message': 'apikey could not be generated'})
        rows = cursor.fetchall()
        if len(rows) > 0:
            authorized = True
        connection.close()
        cursor.close()
        return authorized

    def get_pandas_dataframe(self):
        """ This function loads the ingetsed dataset and cleanses amnd structures the data and generates a dataframe.

        :return: dataframe of the entire cleansed data which was processed from the ingested dataset usign pandas.
        """
        if 'large' in self.file_size:
            data_frame = dd.read_csv('amazon_reviews_us_Software_v1_00.tsv', sep='\t', error_bad_lines=False).compute()
            data_frame.info()
        else:
            url = "https://s3.amazonaws.com/amazon-reviews-pds/tsv/sample_us.tsv"
            url_response_content = requests.get(url).content
            data_frame = pd.read_csv(io.StringIO(url_response_content.decode('utf-8')), sep='\t')

        return data_frame

    def get_market_place_review_id_data(self, marketdata, marketplace, reviewid):
        """ GET market place data for a specific review.

        :param marketdata: The data object on which the query to fetch data is performed.
        :param marketplace: The country on which the filter is to be applied.
        :param reviewid: The review id of the revies for which the data is requested
        :return: JSON data of the specific request.
        """
        jsondat = {}
        dt = marketdata[(marketdata.marketplace == marketplace) & (marketdata.review_id == reviewid)][
            ['customer_id', 'review_id', 'product_id', 'star_rating']]
        if len(dt) > 0:
            for d in dt:
                value = str(str(dt[d]).split('\nName')[0]).split('    ')[1].replace("'", "").strip()
                if value.isdigit():
                    jsondat[d] = int(value)
                else:
                    jsondat[d] = value

            return jsonify({"results": jsondat})
        else:
            return self.make_error(404, 'review for {:} id was not found'.format(reviewid))
            # abort(404, {'message': 'review for {:} id was not found'.format(reviewid)})

    def get_entire_data_for_a_market(self, marketdata, marketplace, limit=None):
        """

        :param marketdata: The data object on which the query to fetch data is performed.
        :param marketplace: The country on which the filter is to be applied.
        :param limit: Limit query parameter sets the limit on the number of records to fetch.
        :return: JSON data of the specific request.
        """
        dict = []
        if limit:
            dt = marketdata[(marketdata.marketplace == marketplace)].head(int(limit))
        else:
            dt = marketdata[(marketdata.marketplace == marketplace)]
        if len(dt) > 0:
            for i in range(len(dt)):
                jsondat = {}
                for d in dt.iloc[[i]]:
                    value = str(str(dt.iloc[[i]][d]).split('\nName')[0]).split('    ')[1].replace("'", "").replace(
                        "\n1",
                        "").strip()
                    if value.isdigit():
                        jsondat[d] = int(value)
                    else:
                        jsondat[d] = value
                dict.append(jsondat)
            return jsonify({"results":dict})
        else:
            return self.make_error(404, 'country {:} dosent exist or please check case'.format(marketplace))
            # abort(404, {'message': 'country {:} dosent exist or please check case'.format(marketplace)})

    def get_entire_data_from_dataframe(self, marketdata, limit=None):
        """

        :param marketdata: The data object on which the query to fetch data is performed.
        :param limit: Limit query parameter sets the limit on the number of records to fetch.
        :return: JSON data of the specific request.
        """
        dict = []
        if limit:
            dt = marketdata.head(int(limit))
        else:
            dt = marketdata
        if len(dt) > 0:
            for i in range(len(dt)):
                jsondat = {}
                for d in dt.iloc[[i]]:
                    value = str(str(dt.iloc[[i]][d]).split('\nName')[0]).split('    ')[1].replace("'", "").replace(
                        "\n1",
                        "").strip()
                    if value.isdigit():
                        jsondat[d] = int(value)
                    else:
                        jsondat[d] = value
                dict.append(jsondat)
            return jsonify({"results":dict})
        else:
            return jsonify({})

    def get_object_data_with_keyword(self, marketdata, object_to_ckeck, keyword):
        """This method is used to check on a column and apply filter on the string content.

        :param marketdata: The data object on which the query to fetch data is performed.
        :param object_to_ckeck: Column/Object name to check.
        :param keyword: Object keys string to filter on.
        :return: JSON data of the specific request.
        """
        dict = []
        dt = marketdata[marketdata['{:}'.format(object_to_ckeck)].str.contains(keyword, na=False)][
            ['customer_id', 'review_id', 'product_id', 'review_body', 'star_rating']]
        if len(dt) > 0:
            for i in range(len(dt)):
                jsondat = {}
                for d in dt.iloc[[i]]:
                    value = str(str(dt.iloc[[i]][d]).split('\nName')[0]).split('    ')[1].replace("'", "").replace(
                        "\n1",
                        "").strip()
                    if value.isdigit():
                        jsondat[d] = int(value)
                    else:
                        jsondat[d] = value
                dict.append(jsondat)
            return jsonify({"results":dict})
        else:
            return self.make_error(404, 'no string found with the request keyword - {:}'.format(keyword))
            # abort(404, {'message': 'no string found with the request keyword - {:}'.format(keyword)})

    def make_error(self, status_code, message):
        response = jsonify({
            'status': status_code,
            'message': message,
        })
        response.status_code = status_code
        return response