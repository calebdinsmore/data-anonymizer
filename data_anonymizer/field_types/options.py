from . import BaseFieldType
from .decorators import apply_formatting_options


class Options(BaseFieldType):
    def __init__(self, type_config_dict):
        super().__init__(type_config_dict)
        options = type_config_dict.get('options')
        if options is None:
            raise ValueError('Options field type must have an options list property defined')
        self.options = options

    @apply_formatting_options
    def generate_obfuscated_value(self, key, value):
        self.seed_faker(key, value)
        return self.faker.random_element(self.options)
