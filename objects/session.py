from models.sessions_model import SessionsModel
from objects.abstract_model_object import AbstractModelObject


class Session(AbstractModelObject):
    attributes = {
        'id': None,
        'user_id': None,
        'created_on': None,
        'updated_on': None
    }
    required_attributes = [
        'user_id'
    ]
    _model = SessionsModel()
