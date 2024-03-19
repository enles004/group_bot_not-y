import time
from datetime import datetime, timedelta

import schedule
import telebot

import config
from db.models import Schedule
from db.session_db import session

bot = telebot.TeleBot(config.token_tele)
message_id = 1457896502


def check_day():
    day = datetime.now()
    tomorrow = day + timedelta(1)
    return tomorrow.strftime("%a")


def job():
    item = {}
    tmr = check_day()
    item["tmr"] = tmr
    sub_of_today = session.query(Schedule).filter_by(day=item["tmr"]).all()
    convert = ["|Sub: {}|Lesson: {}|Room: {}|".format(item.subject, item.lesson, item.room) for item in
               sub_of_today]
    if convert:
        text = "\n".join(convert)
        bot.send_message(message_id, text="Nhung mon hoc ngay mai cua ban")
        bot.send_message(message_id, text=text)
    else:
        bot.send_message(message_id, text="Choi de ban oi")


schedule.every().day.at("22:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
