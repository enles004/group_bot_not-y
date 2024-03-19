import telebot

import config
from handler.schedule import add_schedule, view_schedule, delete_schedule_all, delete_schedule_id

bot = telebot.TeleBot(config.token_tele)

status = None
day = None
count = None
par_item = {}
result = []
i = 1


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
        for item in data:
            view_str += "id{}. |Day: {}|Sub: {}|Les: {}|Room: {}| \n".format(item["id"], item["Day"], item["Sub"],
                                                                             item["Les"],
                                                                             item["Room"])
        bot.send_message(message.chat.id, text=view_str)
        bot.send_message(message.chat.id,
                         text="/add_schedule de them mon hoc.\n/delete_id de xoa mon hoc theo id\n/delete_all de xoa tat ca cac mon hoc")
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
    global count
    bot.reply_to(message, text=f"You chosen {message.text}.")
    day = str(message.text).strip("/").title()
    bot.send_message(message.chat.id, "Nhap so mon ban muon nhap")
    count = "vao viec"


@bot.message_handler(commands=["remove_schedule"])
def remove_schedule(message):
    bot.reply_to(message, f"Da xoa lich {message.text}")


@bot.message_handler(func=lambda msg: True)
def reply(message):
    global status
    global count
    global par_item
    global result
    global i

    if count == "vao viec":
        count = int(message.text)
        status = "add_subject"

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
                message.text = 1
                result.append(par_item)
                par_item = {}

            count -= 1
            i += 1
        i = 1
        add_schedule(data=result, day=day)
        bot.send_message(message.chat.id, text=f"Ban da nhap xong {result}")
        par_item = {}
        result = []
        return
    elif status == "delete_id":
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

        delete_schedule_id(new_data)
        bot.send_message(message.chat.id, text="Ban da xoa thanh cong cac mon hoc theo id")
        status = None
        return

    bot.send_message(message.chat.id, "Toi khong hieu ban muon gi")


bot.infinity_polling()
