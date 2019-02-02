CREATE DATABASE dockerdb;
use dockerdb;

CREATE TABLE marketplace_reviews (
  marketplace VARCHAR(20),
  customer_id VARCHAR(20),
  review_id VARCHAR(20),
  product_id VARCHAR(20),
  product_parent VARCHAR(20),
  product_title VARCHAR(20),
  product_category VARCHAR(20),
  star_rating VARCHAR(20),
  helpful_votes VARCHAR(20),
  total_votes VARCHAR(20),
  vine VARCHAR(20),
  verified_purchase VARCHAR(20),
  review_headline VARCHAR(20),
  review_body VARCHAR(20),
  review_date VARCHAR(20)
);

CREATE TABLE userbase (
  apikey VARCHAR(36) PRIMARY KEY,
  username VARCHAR(20)
);