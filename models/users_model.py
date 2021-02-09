import settings
from models.abstract_model import AbstractModel


class UsersModel(AbstractModel):
    table_name = settings.USERS_TABLE
