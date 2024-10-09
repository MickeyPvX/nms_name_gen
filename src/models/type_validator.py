"""TypeValidator base model"""

from .validator import Validator


class TypeValidator(Validator):
    """Checks type of value against valid types"""

    def __set__(self, instance, value):
        """Setter with type checking"""
        if isinstance(value, self.valid_type):
            instance.__dict__[self.name] = value
        else:
            raise TypeError(f"{instance.__class__.__name__}.{self.name} must be of type(s) {self.valid_str}")
