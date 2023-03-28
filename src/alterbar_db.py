from sqlalchemy import (
    Integer,
    String,
    Column,
    ForeignKey,
    create_engine,
    Boolean,
    BigInteger,
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from alterbar_settings import settings

__engine = create_engine(settings.database_connect_string)

__Base = declarative_base()


class Employee(__Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(length=100))
    last_name = Column(String(length=100))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    tg_user_id = Column(BigInteger, nullable=False, unique=True)


class Currency(__Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True)
    name_short = Column(String(length=10), nullable=False, unique=True)
    name_full = Column(String(length=100), nullable=False, unique=True)


class Unit(__Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True)
    name_short = Column(String(length=10), nullable=False, unique=True)
    name_full = Column(String(length=100), nullable=False, unique=True)


class Category(__Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False, unique=True)


class Product(__Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    price = Column(String(length=100), nullable=False)
    currency = relationship("Currency")
    currency_id = Column(Integer, ForeignKey("currencies.id"))
    quantity = Column(Integer, default=0)
    unit = relationship("Unit")
    unit_id = Column(Integer, ForeignKey("units.id"))
    category = relationship("Category")
    category_id = Column(Integer, ForeignKey("categories.id"))


__authorizedUserIDs = []
__Base.metadata.create_all(__engine)
__Session = sessionmaker()
__Session.configure(bind=__engine)
session = __Session()


def __databaseHasUsers() -> int:
    users = session.query(Employee.tg_user_id).filter_by(is_active=True).all()
    return len(users)


def checkUserID(tg_user_id) -> bool:
    return tg_user_id in __authorizedUserIDs


def databaseInit() -> None:
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


def updateAuthorizedUserIDs() -> None:
    global __authorizedUserIDs
    tg_user_ids_db = session.query(Employee.tg_user_id).filter_by(is_active=True).all()
    # SQLAlchemy returns list of tuples
    __authorizedUserIDs = [cur[0] for cur in tg_user_ids_db]


def getAllUsers() -> list():
    return session.query(Employee).all()


def getUserByID(tg_user_id: int) -> Employee:
    return session.query(Employee).filter_by(tg_user_id=tg_user_id).first()


def renameUserByID(tg_user_id: int, first_name: str, last_name: str) -> None:
    employee = getUserByID(tg_user_id)
    employee.first_name = first_name
    employee.last_name = last_name
    session.commit()


def toggleAdminByID(tg_user_id: int) -> None:
    employee = getUserByID(tg_user_id)
    employee.is_admin = not employee.is_admin
    session.commit()


def deleteUserByID(tg_user_id: int) -> None:
    session.query(Employee).filter_by(tg_user_id=tg_user_id).delete()
    session.commit()


def getAllCategories() -> list():
    return session.query(Category).all()


def getAllUnits() -> list():
    return session.query(Unit).all()


def getUnitByID(unit_id: int) -> Unit:
    return session.query(Unit).get(unit_id)


def addUnit(short_name: str, full_name: str) -> None:
    newUnit = Unit(
        name_short=short_name,
        name_full=full_name,
    )
    session.add(newUnit)
    session.commit()


def changeUnitShortNameByID(unit_id: int, short_name: str) -> None:
    unit = getUnitByID(unit_id)
    unit.name_short = short_name
    session.commit()


def changeUnitFullNameByID(unit_id: int, full_name: str) -> None:
    unit = getUnitByID(unit_id)
    unit.name_full = full_name
    session.commit()


def deleteUnitByID(unit_id: int) -> None:
    session.query(Unit).filter(Unit.id == unit_id).delete()
    session.commit()


def getAllCurrencies() -> list():
    return session.query(Currency).all()


def getCurrencyByID(currency_id: int) -> Currency:
    return session.query(Currency).get(currency_id)


def addCurrency(short_name: str, full_name: str) -> None:
    newCurrency = Currency(
        name_short=short_name,
        name_full=full_name,
    )
    session.add(newCurrency)
    session.commit()


def changeCurrencyShortNameByID(currency_id: int, short_name: str) -> None:
    currency = getCurrencyByID(currency_id)
    currency.name_short = short_name
    session.commit()


def changeCurrencyFullNameByID(currency_id: int, full_name: str) -> None:
    currency = getCurrencyByID(currency_id)
    currency.name_full = full_name
    session.commit()


def deleteCurrencyByID(currency_id: int) -> None:
    session.query(Currency).filter(Currency.id == currency_id).delete()
    session.commit()


def databaseCloseSession() -> None:
    session.close()
