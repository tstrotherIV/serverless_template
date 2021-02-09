class Object:
    class Null:
        pass

    attributes = {}
    protected_attributes = []

    def __init__(self, attributes={}):
        for key, value in self.attributes.items():
            self.__dict__[key] = value
        self.deserialize(attributes)

    def __getattribute__(self, key):
        value = super().__getattribute__(key)
        if value is Object.Null:
            return None
        else:
            return value

    def __setattr__(self, key, value):
        if key not in self.attributes:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, key))
        if value is None:
            self.__dict__[key] = Object.Null
        else:
            self.__dict__[key] = value

    def copy(self):
        return self.__class__(self.serialize(hide_protected_attributes=False))

    def serialize(self, hide_protected_attributes=True):
        attributes = dict()
        for key, value in self.__dict__.items():
            if value is not None:
                if value is Object.Null:
                    attributes[key] = None
                else:
                    attributes[key] = value
        if hide_protected_attributes:
            for key in self.protected_attributes:
                attributes.pop(key, None)

        return attributes

    def deserialize(self, attributes={}):
        for key, value in attributes.items():
            if value is None:
                self.__setattr__(key, self.attributes.get(key, None))
            else:
                self.__setattr__(key, value)

    @classmethod
    def bulk_serialize(cls, objects):
        dicts = []
        for obj in objects:
            dicts.append(obj.serialize())
        return dicts

    @classmethod
    def bulk_deserialize(cls, dicts):
        objects = []
        for dic in dicts:
            objects.append(cls(dic))
        return objects
