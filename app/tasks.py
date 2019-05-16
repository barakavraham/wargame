from app import create_app, db
from app.models.user import User
from datetime import datetime
from time import sleep

app = create_app()
app.app_context().push()


def gift_users_task():
    current_minutes = None
    while True:
        minutes = datetime.utcnow().minute
        if minutes == 0 or minutes == 30:
            if current_minutes is None or minutes != current_minutes:
                current_minutes = minutes
                for user in User.query.all():
                    user.get_gift()
        db.session.commit()
        sleep(1)
