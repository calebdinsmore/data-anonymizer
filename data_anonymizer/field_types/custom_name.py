from . import BaseFieldType
from .decorators import apply_formatting_options


class CustomName(BaseFieldType):
    def __init__(self, type_config_dict):
        super().__init__(type_config_dict)
        self.format_string = type_config_dict.get('format')

    @apply_formatting_options
    def generate_obfuscated_value(self, key, value):
        self.seed_faker(key, value)
        if not self.format_string:
            return self.faker.name()
        else:
            return_value = self.format_string.replace('$FIRST', self.faker.first_name())
            return_value = return_value.replace('$LAST', self.faker.last_name())
            return_value = return_value.replace('$MI', self.faker.lexify('?').upper())
            return_value = self.faker.bothify(return_value)
            return return_value
