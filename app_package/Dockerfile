FROM python:3.6

EXPOSE 5000

WORKDIR /app_package

COPY requirements.txt /app_package
RUN pip install -r requirements.txt
RUN pip install dask[complete] distributed --upgrade

#RUN wget https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Software_v1_00.tsv.gz \
#&& gunzip -k amazon_reviews_us_Software_v1_00.tsv.gz && rm amazon_reviews_us_Software_v1_00.tsv.gz

COPY app.py /app_package
COPY app_worker.py /app_package
COPY app_dal.py /app_package
COPY test_suit.py /app_package

CMD python -m test_suit.py
CMD python app.py