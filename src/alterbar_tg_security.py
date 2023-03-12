import sqlalchemy
import alterbar_db


def checkUserID(userID):
    userIDsDB = (
        alterbar_db.session.query(alterbar_db.Employee.tg_user_id)
        .filter_by(is_active=True)
        .all()
    )
    # SQLAlchemy returns list of tuples
    userIDs = [cur[0] for cur in userIDsDB]
    return userID in userIDs
