class Validator(object):

    def __init__(self, valid_type, nullable=False):
        self.valid_type = self._tuplator(valid_type)
        self.nullable = nullable

        if nullable:
            self.valid_type = self.valid_type + (type(None),)

        self.valid_str = self._valid_types()

    def __get__(self, instance, owner):
        if self.name in instance.__dict__:
            return instance.__dict__[self.name]
        else:
            raise AttributeError(f'{instance.__class__.__name__} has no attribute "{self.name}"')

    def __set__(self, instance, value):
        raise NotImplementedError

    def __set_name__(self, owner, name):
        self.name = name

    def _valid_types(self):
        type_list = ['None'] if self.nullable else []

        try:
            type_list.extend([valid.__name__ for valid in iter(self.valid_type)])
        except TypeError:
            type_list.append(self.valid_type.__name__)

        return type_list

    def _tuplator(self, value):
        value_cls = value.__class__
        tuple_map = {
            type: lambda x: (x,),
            list: lambda x: tuple(x),
            set: lambda x: tuple(x),
            bool: lambda x: (x.__class__,),
            int: lambda x: (x.__class__,)
        }

        return tuple_map.get(value_cls, lambda x: x)(value)
