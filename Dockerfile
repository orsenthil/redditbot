FROM python:3.7.3-stretch
COPY requirements.txt /tmp/

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

COPY templates/ /templates/
COPY redditbot.py .

CMD [ "python", "./redditbot.py" ]
