import sqlalchemy
import alterbar_db

__userIDs = []


def setUserIDs():
    global __userIDs
    userIDsDB = (
        alterbar_db.session.query(alterbar_db.Employee.tg_user_id)
        .filter_by(is_active=True)
        .all()
    )
    # SQLAlchemy returns list of tuples
    __userIDs = [cur[0] for cur in userIDsDB]


def checkUserID(userID):
    return userID in __userIDs
