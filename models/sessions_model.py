import settings
from models.abstract_model import AbstractModel


class SessionsModel(AbstractModel):
    table_name = settings.SESSIONS_TABLE
