import telebot

import config
from handler.schedule import add_schedule, view_schedule, delete_schedule_all, delete_schedule_id

bot = telebot.TeleBot(config.token_tele)

status = None
day = None
day_int = None
count = None
par_item = {}
result = []
data_del = []
i = 1
j = 0


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, day la chuong trinh bot_telegram thong bao thoi khoa bieu.")
    bot.send_message(message.chat.id, text="/add_schedule\n/view_schedule")


@bot.message_handler(commands=["add_schedule"])
def add_sche(message):
    text = "Chon ngay.\n/mon\n/tue\n/wed\n/thu\n/fri"
    bot.reply_to(message, text=text)


@bot.message_handler(commands=["view_schedule"])
def view_sche(message):
    data = view_schedule()
    if data:
        view_str = ""
        global j
        for item in data:
            j += 1
            view_str += f"{j}. " + "|Day: {}|Sub: {}|Les: {}|Room: {}| \n".format(item["Day"], item["Sub"],
                                                                                  item["Les"],
                                                                                  item["Room"])

            item_del = {"day": item["Day"], "subject": item["Sub"], "lesson": item["Les"], "room": item["Room"]}
            data_del.append(item_del)
        j = 0
        bot.send_message(message.chat.id, text=view_str)
        bot.send_message(message.chat.id,
                         text="/add_schedule de them mon hoc.\n/delete_id de xoa mon hoc theo id\n/delete_all de xoa "
                              "tat ca cac mon hoc")
        return
    bot.send_message(message.chat.id, text="Thoi khoa bieu cua ban khong co du lieu")
    bot.send_message(message.chat.id, text="/add_schedule de them cac mon hoc")
    return


@bot.message_handler(commands=["delete_all", "delete_id"])
def delete_subject(message):
    global status
    if message.text == "/delete_all":
        delete_schedule_all()
        bot.send_message(message.chat.id, text="Ban da xoa thanh cong cac mon hoc")
        return
    elif message.text == "/delete_id":
        bot.send_message(message.chat.id, text="nhap cac id muon xoa cach nhau bang dau ','\nVi du: 1, 2, 3, 4 ...")
        status = "delete_id"
        return


@bot.message_handler(commands=["mon", "tue", "wed", "thu", "fri"])
def add_schedule_with_day(message):
    global status
    global day
    global day_int
    global count
    bot.reply_to(message, text=f"You chosen {message.text}.")
    day = str(message.text).strip("/").title()
    if day == "Mon":
        day_int = 2
    elif day == "Tue":
        day_int = 3
    elif day == "Wed":
        day_int = 4
    elif day == "Thu":
        day_int = 5
    elif day == "Fri":
        day_int = 6
    bot.send_message(message.chat.id, "Nhap so mon ban muon nhap")
    status = "vao viec"


@bot.message_handler(func=lambda msg: True)
def reply(message):
    global status
    global count
    global par_item
    global result
    global i

    if status == "vao viec":
        try:
            if isinstance(int(message.text), int):
                count = int(message.text)
            status = "add_subject"
        except ValueError:
            bot.reply_to(message, "Ban nhap sai lua chon")
            return
    if status == "add_subject":
        while count > 0:
            if "subject" not in par_item:
                try:
                    if isinstance(int(message.text), int):
                        bot.send_message(message.chat.id, f"Moi ban nhap subjects {i}: ")
                        return
                except ValueError:
                    par_item["subject"] = message.text
                    bot.send_message(message.chat.id, f"Moi ban nhap lesson {i}: ")
                    return

            if "lesson" not in par_item:
                par_item["lesson"] = message.text
                bot.send_message(message.chat.id, f"Moi ban nhap room {i}: ")
                return

            if "room" not in par_item:
                par_item["room"] = message.text
                par_item["day"] = day
                par_item["day_int"] = day_int
                message.text = 1
                result.append(par_item)
                par_item = {}

            count -= 1
            i += 1
        i = 1
        add_schedule(data=result)
        bot.send_message(message.chat.id, text=f"Ban da nhap xong {result}")
        par_item = {}
        result = []
        status = None
        return

    elif status == "delete_id":
        global data_del
        solve_text = str(message.text).split(",")
        new_data = []
        for item in solve_text:
            try:
                isinstance(int(item), int)
                new_data.append(int(item))
            except ValueError:
                bot.reply_to(message, text="Hinh nhu ban nhap sai cu phap")
                bot.send_message(message.chat.id, text="/delete_id de thuc hien lai")
                return

        delete_schedule_id(new_data, data_del=data_del)
        data_del = []
        bot.send_message(message.chat.id, text="Ban da xoa thanh cong cac mon hoc theo id")
        status = None
        return

    bot.send_message(message.chat.id, "Toi khong hieu ban muon gi")


bot.infinity_polling()
