import feedparser, smtplib
from email.mime.text import MIMEText
import os

def fetch_jobs():
    feeds = [
        'https://aijobs.ai/rss?level=entry',
        'https://topstartups.io/jobs/feed/',
    ]
    jobs = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.title.lower()
            if any(keyword in title for keyword in ['data', 'ml', 'machine learning']):
                jobs.append(f"{entry.title}\n{entry.link}")
    # Remove duplicates
    return list(dict.fromkeys(jobs))

def send_email(jobs):
    sender = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASS']
    recipient = os.environ.get('EMAIL_TO', sender)

    body = "\n\n".join(jobs)
    msg = MIMEText(body)
    msg['Subject'] = '🧠 Daily AI/ML Entry-Level Jobs'
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

if __name__ == "__main__":
    jobs = fetch_jobs()
    if jobs:
        send_email(jobs)
    else:
        print("No matching jobs found today.")
