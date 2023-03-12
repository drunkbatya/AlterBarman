from pydantic import BaseModel, ValidationError, validator
from environs import Env


class Settings(BaseModel):
    telegram_token: str
    database_connect_string: str
    admin_user_telegram_id: int

    @validator("*", each_item=True)
    def emptyString(cls, elem):
        if isinstance(elem, str):
            if not elem or elem.isspace():
                raise ValueError("Variable is empty")
        return elem


__env = Env()
__env.read_env()
settings = Settings(
    telegram_token=__env("TELEGRAM_TOKEN"),
    database_connect_string=__env("DATABASE_CONNECT_STRING"),
    admin_user_telegram_id=__env("ADMIN_USER_TELEGRAM_ID"),
)
