from objects.object import Object


class RequiredAttributes(Exception):
    pass


class AbstractModelObject(Object):
    required_attributes = []
    _model = None

    def __init__(self, attributes_or_id={}):
        if type(attributes_or_id) is dict:
            super().__init__(attributes_or_id)
        elif type(attributes_or_id) is str:
            super().__init__(self._model.get(attributes_or_id))

    def save(self):
        if self.id and bool(self._model.get(self.id)):
            # update
            self.deserialize(self._model.update(self.id, self.serialize(hide_protected_attributes=False)))
        else:
            # insert
            missing_attributes = self._get_missing_attributes()
            if missing_attributes:
                raise RequiredAttributes('missing the following required attributes: ' + ', '.join(missing_attributes))
            self.deserialize(self._model.insert(self.serialize(hide_protected_attributes=False)))

    def delete(self):
        if self.id:
            return self._model.delete(self.id)
        else:
            return False

    def _get_missing_attributes(self):
        missing_attributes = []
        for required_attribute in self.required_attributes:
            if self.__dict__.get(required_attribute, None) is None:
                missing_attributes.append(required_attribute)
        return missing_attributes
