import time
from datetime import datetime, timedelta
from db.session_db import schedule
import schedule
import telebot
from handler.news import news
import config

bot = telebot.TeleBot(config.token_tele)
group_id = -4019357479


def check_day():
    day = datetime.now()
    tomorrow = day + timedelta(1)
    return tomorrow.strftime("%a")


def job():
    item = {}
    tmr = check_day()
    item["tmr"] = tmr
    sub_of_today = list(schedule.find({"day": item["tmr"]}).sort("lesson", -1))
    convert = ["|Sub: {}|Lesson: {}|Room: {}|".format(item["subject"], item["lesson"], item["room"]) for item in
               sub_of_today]
    if convert:
        text = "\n".join(convert)
        bot.send_message(group_id, text="Nhung mon hoc ngay mai")
        bot.send_message(group_id, text=text)
    else:
        bot.send_message(group_id, text="Choi de cac ban oi, mai duoc nghi.")


schedule.every().day.at("22:00").do(job)
schedule.every().day.at("06:00").do(news)
while True:
    schedule.run_pending()
    time.sleep(1)
