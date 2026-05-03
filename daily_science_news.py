import os
import smtplib
from email.mime.text import MIMEText
from newsapi import NewsApiClient

# 读取环境变量（设置为 GitHub Action Secrets）
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")
EMAIL_USER = os.environ.get("EMAIL_USER") or "3208696438@qq.com"
EMAIL_PASS = os.environ.get("EMAIL_PASS")
TO_ADDR = os.environ.get("TO_ADDR") or "3208696438@qq.com"

EMAIL_HOST = "smtp.qq.com"
EMAIL_PORT = 587

def fetch_science_news(num=20):
    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
    all_articles = newsapi.get_top_headlines(
        category='science',
        language='en',
        page_size=num,
    )
    news_list = []
    for article in all_articles['articles']:
        news_list.append((article['title'], article['description'], article['url'], article['source']['name']))
    return news_list

def send_email(news):
    subject = "每日全球科学新闻日报"
    body = ""
    for idx, (title, desc, url, source) in enumerate(news, 1):
        body += f"{idx}. [{title}]({url})\n来源：{source}\n摘要：{desc or '无'}\n\n"
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = TO_ADDR
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, TO_ADDR, msg.as_string())

if __name__ == "__main__":
    news = fetch_science_news(20)
    send_email(news)
