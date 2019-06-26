from app import db, bcrypt
from app.models.user import User
from app.models.army import Army, Upgrade


def create_user(email, password, army_name):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    army = Army(user_id=user.id, name=army_name)
    db.session.add(army)
    db.session.commit()
    upgrade = Upgrade(army_id=army.id)
    db.session.add(upgrade)
    db.session.commit()
    return user