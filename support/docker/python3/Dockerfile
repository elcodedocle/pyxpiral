FROM python:3-alpine

ENV LIBRARY_PATH=/lib:/usr/lib
RUN apk --update add --no-cache build-base python3-dev zlib-dev jpeg-dev git \
&& pip install pytest pytest-cov pylint mock \
&& rm -rf /var/cache/apk/*
ENTRYPOINT ["/bin/sh", "-c", "git clone https://github.com/elcodedocle/pyxpiral.git  && cd pyxpiral &&  git checkout development && pip install -r requirements.txt && py.test -vv --cov=pyxpiral --cov-config .coveragerc --cov-report term --cov-report html"]
