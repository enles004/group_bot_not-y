from db.models import Schedule
from db.session_db import session


def add_schedule(data, day):
    for item in data:
        new_schedule = Schedule(**item, day=day)
        session.add(new_schedule)
        session.commit()


def view_schedule():
    schedule = session.query(Schedule).all()
    data_schedule = [{"Day": item.day, "Sub": item.subject, "Les": item.lesson, "Room": item.room, "id": item.id} for
                     item in schedule]
    return data_schedule


def delete_schedule_all():
    session.query(Schedule).delete()
    session.commit()


def delete_schedule_id(input_data):
    for item in input_data:
        sub = session.query(Schedule).get(item)
        session.delete(sub)
        session.commit()
