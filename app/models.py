from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app import login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


workout_exercises = db.Table(
    'workout_exercises',
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id')),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'))
)


class Exercise(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                            unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(256))
    image: so.Mapped[str] = so.mapped_column(sa.String(256))
    alt: so.Mapped[str] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<Exercise {}>'.format(self.name)


class Workout(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                            unique=True)
    exercise_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Exercise.id))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id))
