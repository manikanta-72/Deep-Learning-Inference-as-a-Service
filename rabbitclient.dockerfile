FROM python:3.8-slim

ENV PYTHONUNBUFFERED True
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV APP_HOME /rabbit_client
WORKDIR $APP_HOME
COPY . ./

CMD ["python","receiver_queue.py"]