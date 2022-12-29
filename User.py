from sqlalchemy.dialects.postgresql import (
    INTEGER,
    TEXT,
    NUMERIC
)


from db_init import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer(), primary_key=True)
    name_ = db.Column(TEXT)
    email = db.Column(TEXT, nullable=False, unique=True)
    psw = db.Column(TEXT, nullable=False)

    def __init__(self, name_, email, psw):
        self.name_ = name_
        self.email = email
        self.psw = psw


    def __repr__(self):
        return "<{}:{}>".format(self.user_id, self.name_)




