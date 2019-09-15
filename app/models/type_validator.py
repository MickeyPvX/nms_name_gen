from .validator import Validator


class TypeValidator(Validator):

    def __set__(self, instance, value):
        if isinstance(value, self.valid_type):
            instance.__dict__[self.name] = value
        else:
            raise TypeError(f'{instance.__class__.__name__}.{self.name} must be of type(s) {self.valid_str}')
