FROM tiangolo/uwsgi-nginx-flask:python3.6
COPY ./app /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN wget http://download.redis.io/redis-stable.tar.gz \
    && tar xvzf redis-stable.tar.gz \
    && cd redis-stable \
    && make \
    && make install
RUN python3 db_config.py && python3 lotsofdata.py

