from datetime import date
import datetime as datetime21
today = date.today()
crawl_date = today.strftime("%Y%m%d")
today_news = date.today() - datetime21.timedelta(1)

print(today_news.day)