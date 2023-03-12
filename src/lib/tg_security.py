import sqlalchemy
from . import db


def checkUserID(userID):
    userIDsDB = db.session.query(db.Employee.tg_user_id).filter_by(is_active=True).all()
    # SQLAlchemy returns list of tuples
    userIDs = [cur[0] for cur in userIDsDB]
    return userID in userIDs
