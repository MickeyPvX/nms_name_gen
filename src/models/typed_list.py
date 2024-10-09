"""TypedList type validator"""

from .validator import Validator


class TypedList(Validator):
    """TypedList checks if the value is a List of a certain sub-type"""

    def __set__(self, instance, value):
        """Setter with type checking"""
        if isinstance(value, list) and all(isinstance(item, self.valid_type) for item in value):
            instance.__dict__[self.name] = value
        else:
            raise TypeError(f"{instance.__class__.__name__}.{self.name} must be a list of {self.valid_str}")
