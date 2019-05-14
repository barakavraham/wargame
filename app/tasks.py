from app import db
from app.models import User
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from time import sleep
import math


def gift_users():
    # add code to gift all users whatever you want
    for user in User.query.all():
        user.army.gold += math.ceil(user.army.field/10)
        user.army.metal += math.ceil(user.army.field/20)
        user.army.wood += math.ceil(user.army.field/20)
        user.army.turns += 3
        db.session.commit()


def gift_users_task():
    current_minutes = None
    while True:
        minutes = datetime.utcnow().minute
        if minutes == 0 or minutes == 30:
            if current_minutes is None or minutes != current_minutes:
                current_minutes = minutes
                gift_users()
        sleep(1)


scheduler = BackgroundScheduler()
# scheduler.add_job(gift_users_task)
