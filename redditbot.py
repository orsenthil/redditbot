import os
import smtplib
import ssl
import sys

from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import praw

SUBREDDIT_SOURCE = 'coronavirus'

REQUIRED_ENVVARS = ["REDDIT_USERNAME",
                    "REDDIT_PASSWORD",
                    "REDDIT_API_CLIENT_SECRET",
                    "REDDIT_API_CLIENT_ID",
                    "SENDER_EMAIL",
                    "SENDER_NAME",
                    "SENDER_EMAIL_PASSWORD",
                    "RECEIVER_EMAIL"]

for envvar in REQUIRED_ENVVARS:
    missing_envvars = []
    if envvar not in os.environ:
        missing_envvars.append(envvar)
    if missing_envvars:
        print(f"Missing Environment Variables: {missing_envvars}")
        sys.exit(1)


REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_API_CLIENT_SECRET = os.getenv("REDDIT_API_CLIENT_SECRET")
REDDIT_API_CLIENT_ID = os.getenv("REDDIT_API_CLIENT_ID")

# API CONSTANTS
SMTP_GMAIL_COM = "smtp.gmail.com"
USER_AGENT = f'testscript by /u/{REDDIT_USERNAME}'

# Email CONSTANTS
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME")
SENDER_EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD")


def format_for_plain_text_email(titles, urls):
    with open('templates/txt.tmpl') as f:
        text = f.read()

    messages = []
    for title, url in zip(titles, urls):
        news = "* {title} - {url}".format(title=title, url=url)
        messages.append(news)

    news = "\n".join(messages)

    return text.format(news=news)


def format_for_html_email(message_title, titles, urls):
    with open('templates/html.tmpl') as f:
        html = f.read()

    messages = [
        "<ul>"
    ]

    for title, url in zip(titles, urls):
        news = "<p> <font size='4'> {title} </font> <br> Source: {url} </p> <br/>"
        news = news.format(title=title, url=url)
        messages.append(news)

    messages.append("</ul>")

    return html.format(message_title=message_title, news="\n".join(messages))


if __name__ == '__main__':
    now = datetime.now()
    today = now.strftime("%d-%b-%Y")
    message_title = f"Coronavirus News for {today}"

    reddit = praw.Reddit(client_id=REDDIT_API_CLIENT_ID,
                         client_secret=REDDIT_API_CLIENT_SECRET,
                         password=REDDIT_PASSWORD,
                         user_agent=USER_AGENT,
                         username=REDDIT_USERNAME)

    receiver_email = os.environ.get("RECEIVER_EMAIL")

    message = MIMEMultipart("alternative")
    message["Subject"] = message_title
    message["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    message["To"] = receiver_email

    user = reddit.user.me()
    titles = []
    urls = []

    for submission in reddit.subreddit(SUBREDDIT_SOURCE).top(
            time_filter='day', limit=10):
        titles.append(submission.title)
        urls.append(submission.url)

    text = format_for_plain_text_email(titles, urls)
    html = format_for_html_email(message_title, titles, urls)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_GMAIL_COM, 465, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
        server.sendmail(
            SENDER_EMAIL, receiver_email, message.as_string()
        )
