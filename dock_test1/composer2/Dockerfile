FROM python:2.7.15-alpine3.6
WORKDIR /usr/app
RUN pip install redis requests
COPY ./app-server.py ./
COPY ./appy ./
CMD ["/usr/local/bin/python", "app-server.py"]
