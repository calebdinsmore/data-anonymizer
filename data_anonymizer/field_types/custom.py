from . import BaseFieldType
from .decorators.text_formatter import apply_formatting_options


class Custom(BaseFieldType):
    def __init__(self, type_config_dict):
        super().__init__(type_config_dict)
        format_string = type_config_dict.get('format')
        if not format_string or not isinstance(format_string, str):
            raise ValueError('Custom field types must have a format defined of type string')
        self.format = type_config_dict['format']

    @apply_formatting_options
    def generate_obfuscated_value(self, key, value):
        self.seed_faker(key, value)
        return self.faker.bothify(self.format)
