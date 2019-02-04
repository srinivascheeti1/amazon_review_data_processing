# amazon_review_data_processing_doc

## Processing of https://registry.opendata.aws Amazon Customer Reviews dataset
This project is to provide http REST API's for querying data that was ingested, cleansed and stored as part 
of booting up a  multi-container Docker application using **_docker-compose up_** or **_docker-compose up -d_** command. 
The used data set reference (one fo the .gz files) could be found in this [link](https://s3.amazonaws.com/amazon-reviews-pds/tsv/index.txt).

## Prerequisites
* Install _python 3_.
* Install _docker_ and _docker-compose_ if on a new server or system.


## Getting Started
* Clone in to the GIT repository [link](https://github.com/srinivascheeti1/amazon_review_data_processing.git).
* In the root directory, i.e, DOCKER, run the command **docker-compose up**
* In a moment, depending on the size of the data file that is being ingested, you should be ready 
  to make API calls after you notice below lines of trace which means the spinup process is successfull.
    > db_1   | 2019-01-30T05:34:14.977501Z 0 [Note] mysqld: ready for connections.
    > db_1   | Version: '5.7.25'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server (GPL)
* Start with registering a user (refer to ) to get a _apikey_ used as a authentication header.
* The subsequent API calls, will have access to that data which was loaded and cleansed using the provided API key.

## Test condition
* Once the docker container is launched, launch the test_suit using _python test_suit.py_ command.

## Scripts
* init.sql to create required tables in mysql.
* app.py is the entry point to initialize data ingestion, processing (clean and store) and run flask app.
* app_worker.py holds the business logic required
* app_dal.py acts as a Data Access Layer for the application.

## Code HTML Documentaton File
* codebase html document (index.html), documenting the code and links to source code is available under the below structure.
```
    ├── DOCKER_ASSIGN
    │   ├── build
    │   │   ├── html
    │   │   |   ├── index.js
    │   │   |   ├── package.json
```


## Flask Endpoints to query the ingested data 
**Create a user using create user API to get the apikey. This API key is used for authenticating other API's**
 > Use host = 0.0.0.0:5000 if setup is done locally.


**HEADER INFO**:
```
x-api-key: <apikey>
```
* **POST - Create a user**
    * curl  -H "Content-Type: application/json" -d '{"username":"requester_username"}' -X POST http://{host}/v1/data/registeruser
* **GET - Sample reviews with limit, say 10 items**
    * curl -X GET -H "x-api-key: <apikey>" http://{host}/v1/data/marketplace/<marketplace>?limit={limit}
* **GET - entire marketplace reviews count**
    * curl -X GET -H "x-api-key: <apikey>" http://{host}/v1/data/marketplace/reviewcount
* **GET - a limited number of reviews for a marketplace**
    * curl -X GET -H "x-api-key: <apikey>" http://{host}/v1/data/marketplace/{marketplace}?limit={passlimit}
* **GET - some insights into a specific review in a location**
    * curl -X GET -H "x-api-key: <apikey>" http://{host}/v1/data/marketplace/{marketplace}/reviewid/{reviewid}
* **GET - details for a matching string in a object**
    > For example, search object - review_body containing keyword - BB25
    * curl -X GET -H "x-api-key: <apikey>" http://{host}/v1/data/marketplace/object/{obj}/keyword/{keyword}
    

## Built With
```
Flask - Micro web framework.
pandas - Pandas is an open-source, BSD-licensed Python library.
requests - Requests is a python HTTP library.
mysql-connector - MySQL connector library.
dask - Dask is a flexible parallel computing library for analytics.

```

## Authors
* _Srinivas Rao Cheeti_
