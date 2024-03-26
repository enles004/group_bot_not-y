import telebot
import random
import os
import config
from handler.news import news
from handler.schedule import add_schedule, view_schedule, delete_schedule_all, delete_schedule_id

bot = telebot.TeleBot(config.token_tele)
files = os.listdir("gaixinh")
status = None
day = None
day_int = None
count = None
par_item = {}
result = []
data_del = []
i = 1
j = 0
admin = 1457896502
group_id = -4019357479


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.from_user.id == admin:
        bot.send_message(message.chat.id,
                         "Đây là những gì em có thể phục vụ cho ngài. 🥺\n/view_schedule để ngài có thể xem các môn học của UTT. 😉\n/news Em có thể giúp ngài cập nhật thông tin mới nhất ạ.. 😊\nNgài cần gì nè.. 😚")
        return
    if message.chat.id != group_id:
        bot.send_message(message.chat.id, f"Ngài Oh Fuoc không cho em phục vụ {message.chat.username}.")
        return
    bot.reply_to(message, text="Em là Lưu Hạo Tồn, chủ nhân của em là ngài Oh Fuoc. 🥰")
    return


@bot.message_handler(commands=["add_schedule"])
def add_sche(message):
    if message.from_user.id == admin:
        text = "Chon ngay.\n/mon\n/tue\n/wed\n/thu\n/fri"
        bot.reply_to(message, text=text)
        return
    if message.chat.id != group_id:
        bot.send_message(message.chat.id, f"Ngài Oh Fuoc không cho em phục vụ {message.chat.username}.")
        return
    bot.reply_to(message, text="Cu chỉ được xem thôi..")
    return


@bot.message_handler(commands=["imgs"])
def add_image(message):
    global files
    if message.chat.id != group_id and message.chat.id != admin:
        bot.send_message(message.chat.id, f"Ngài Oh Fuoc không cho em phục vụ {message.chat.username}. 😞")
        return
    random_img = random.choice(files)
    path_img = os.path.join("gaixinh", random_img)
    photo = open(path_img, "rb")
    bot.send_photo(message.chat.id, photo)
    files.remove(random_img)
    os.remove(path_img)
    return

@bot.message_handler(commands=["view_schedule"])
def view_sche(message):
    if message.chat.id != group_id and message.from_user.id != admin:
        bot.send_message(message.chat.id, f"Ngài Oh Fuoc không cho em phục vụ {message.chat.username}. 😞")
        return
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
        return
    bot.send_message(message.chat.id, text="Thời khóa biểu không có dữ liệu.")
    bot.send_message(message.chat.id, text="Đợi chủ nhân 'Oh Fuoc' của tôi cho tôi ăn đã. 🤤")
    return


@bot.message_handler(commands=["delete_all", "delete_id"])
def delete_subject(message):
    global status
    if message.from_user.id == admin:
        if message.text == "/delete_all":
            delete_schedule_all()
            bot.send_message(admin, text="Ban da xoa thanh cong cac mon hoc")
            return
        elif message.text == "/delete_id":
            bot.send_message(admin, text="nhap cac id muon xoa cach nhau bang dau ','\nVi du: 1, 2, 3, 4 ...")
            status = "delete_id"
            return
    if message.chat.id != group_id:
        bot.send_message(message.chat.id, f"Ngài Oh Fuoc không cho em phục vụ {message.chat.username}. 😞")
        return
    bot.reply_to(message, text="??? Định làm gì cơ..?")
    return


@bot.message_handler(commands=["mon", "tue", "wed", "thu", "fri"])
def add_schedule_with_day(message):
    global status
    global day
    global day_int
    global count
    if message.from_user.id == admin:
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
        bot.send_message(admin, "Nhap so mon ban muon nhap")
        status = "vao viec"
    elif message.chat.id != group_id or message.from_user.id != admin:
        bot.send_message(message.chat.id, f"Ngài Oh Fuoc không cho em phục vụ {message.chat.username}. 😞")
        return


@bot.message_handler(commands=["news"])
def view_news(message):
    if message.chat.id != group_id:
        bot.send_message(message.chat.id, f"Ngài Oh Fuoc không cho em phục vụ {message.chat.username}. 😞")
        return
    news(message=message, bot=bot)
    return


@bot.message_handler(func=lambda msg: True)
def reply(message):
    global status
    global count
    global par_item
    global result
    global i

    if message.chat.id == admin:
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
                            bot.send_message(admin, f"Moi ban nhap subjects {i}: ")
                            return
                    except ValueError:
                        par_item["subject"] = message.text
                        bot.send_message(admin, f"Moi ban nhap lesson {i}: ")
                        return

                if "lesson" not in par_item:
                    par_item["lesson"] = message.text
                    bot.send_message(admin, f"Moi ban nhap room {i}: ")
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
            bot.send_message(admin, text=f"Ban da nhap xong {result}")
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
                    bot.send_message(admin, text="/delete_id de thuc hien lai")
                    return

            delete_schedule_id(new_data, data_del=data_del)
            data_del = []
            bot.send_message(admin, text="Ban da xoa thanh cong cac mon hoc theo id")
            status = None
            return
    print(message.chat.id)
    if message.from_user.id == admin:
        bot.reply_to(message, text="Dạ thưa chủ nhân, em không biết ngài cần gì ạ.. 🥺")
        return
    bot.send_message(message.chat.id, "Đừng làm những điều vớ vẩn, vì bạn không phải là chủ nhân của tôi. 😌")


bot.infinity_polling()
