import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

YOUR_EMAIL = "RAKESH.GOLLAPALLI5@GMAIL.COM"
YOUR_PASSWORD = "YOUR_APP_PASSWORD"  # Replace with your 16-character App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

JOB_KEYWORDS = ["C++", "Python", "Mainframe"]
JOB_LOCATION = "India"
RSS_FEEDS = [
    f"https://www.indeed.co.in/rss?q={'+'.join(JOB_KEYWORDS)}&l={JOB_LOCATION}"
]

def fetch_jobs():
    jobs = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            jobs.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published
            })
    return jobs

def format_email(jobs):
    if not jobs:
        return "No new job listings today."
    html = "<h2>Daily Job Listings</h2><ul>"
    for job in jobs:
        html += f"<li><a href='{job['link']}'>{job['title']}</a> - {job['published']}</li>"
    html += "</ul>"
    return html

def send_email(content):
    msg = MIMEMultipart()
    msg['From'] = YOUR_EMAIL
    msg['To'] = YOUR_EMAIL
    msg['Subject'] = f"Daily Job Update - {datetime.now().strftime('%d-%b-%Y')}"
    msg.attach(MIMEText(content, 'html'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(YOUR_EMAIL, YOUR_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)

if __name__ == "__main__":
    jobs = fetch_jobs()
    email_content = format_email(jobs)
    send_email(email_content)
