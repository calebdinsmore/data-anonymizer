from . import BaseFieldType


class Custom(BaseFieldType):
    def __init__(self, type_config_dict):
        super().__init__()
        format_string = type_config_dict.get('format')
        if not format_string or not isinstance(format_string, str):
            raise ValueError('Custom field types must have a format defined of type string')
        self.format = type_config_dict['format']

    def generate_obfuscated_value(self, value):
        self.seed_faker(value)
        return self.faker.bothify(self.format)
