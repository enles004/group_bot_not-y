from db.session_db import schedule


def add_schedule(data):
    for item in data:
        schedule.insert_one(item)


def view_schedule():
    schedule_data = schedule.find().sort([("day_int", 1), ("lesson", -1)])
    data = list(schedule_data)
    data_schedule = [{"Day": item["day"], "Sub": item["subject"], "Les": item["lesson"], "Room": item["room"]} for
                     item in data]
    return data_schedule


def delete_schedule_all():
    schedule.delete_many()


def delete_schedule_id(input_data, data_del):
    for item in input_data:
        schedule.delete_one(data_del[item - 1])
