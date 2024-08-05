from datetime import datetime
from app import app, db
from api.models import User, WorkType, Todo

def add_sample_data():
    user = User(id="1", name="xyz", email="xyz@gmail.com", password="cvb", premium=False)
    db.session.add(user)
    db.session.commit()

    work = WorkType(id=1, name="w1", user_id=user.id)
    db.session.add(work)
    db.session.commit()

    todo = Todo(
        id=1,
        description="Run a marathon",
        completed=False,
        due_date=datetime(2024, 1, 29).date(),
        user_id=user.id,
        worktype_id=work.id,
        image="pic1.png"
    )
    db.session.add(todo)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        add_sample_data()
        print("Sample data added.")
