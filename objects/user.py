from models.users_model import UsersModel
from objects.abstract_model_object import AbstractModelObject


class EmailExists(Exception):
    pass


class User(AbstractModelObject):
    attributes = {
        'id': None,
        'email': None,
        'password': None,
        'created_on': None,
        'updated_on': None
    }
    protected_attributes = [
        'password'
    ]
    required_attributes = [
        'email',
        'password'
    ]
    _model = UsersModel()

    def save(self):
        if self.email:
            existing_user = User()
            existing_user.load_by_email(self.email)
            if existing_user.id:
                if self.id and self.id == existing_user.id:
                    super().save()
                else:
                    raise EmailExists('email already exists')
        super().save()

    def load_by_email(self, email):
        users = self._model.get_all_by_index('email', email)
        if len(users) == 1:
            self.deserialize(users[0])
