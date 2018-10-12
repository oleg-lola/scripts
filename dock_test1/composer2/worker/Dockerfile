FROM python:2.7.15-alpine3.6
WORKDIR /usr/worker
RUN pip install redis requests
COPY ./worker.py ./
CMD ["/usr/local/bin/python", "worker.py"]
