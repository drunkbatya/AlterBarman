import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from alterbar_settings import settings

__engine = sqlalchemy.create_engine(settings.database_connect_string)

__Base = declarative_base()


class Employee(__Base):
    __tablename__ = "employees"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    first_name = sqlalchemy.Column(sqlalchemy.String(length=100))
    last_name = sqlalchemy.Column(sqlalchemy.String(length=100))
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    tg_user_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False, unique=True)


__authorizedUserIDs = []
__Base.metadata.create_all(__engine)
__Session = sqlalchemy.orm.sessionmaker()
__Session.configure(bind=__engine)
session = __Session()


def __databaseHasUsers():
    users = session.query(Employee.tg_user_id).filter_by(is_active=True).all()
    return len(users)


def checkUserID(userID):
    return userID in __authorizedUserIDs


def databaseInit():
    if not __databaseHasUsers():
        newEmployee = Employee(
            first_name="Admin",
            last_name="User",
            tg_user_id=settings.admin_user_telegram_id,
            is_active=True,
            is_admin=True,
        )
        session.add(newEmployee)
        session.commit()


def updateAuthorizedUserIDs():
    global __authorizedUserIDs
    userIDsDB = session.query(Employee.tg_user_id).filter_by(is_active=True).all()
    # SQLAlchemy returns list of tuples
    __authorizedUserIDs = [cur[0] for cur in userIDsDB]


def getAllEmployees():
    return session.query(Employee).all()


def getEmployeeByID(userID):
    return session.query(Employee).filter_by(tg_user_id=userID).first()


def databaseCloseSession():
    session.close()
