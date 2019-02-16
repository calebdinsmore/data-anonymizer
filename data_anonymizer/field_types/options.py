from . import BaseFieldType


class Options(BaseFieldType):
    def __init__(self, type_config_dict):
        super().__init__(type_config_dict)
        options = type_config_dict.get('options')
        if options is None:
            raise ValueError('Options field type must have an options list property defined')
        self.options = options

    def generate_obfuscated_value(self, value):
        self.seed_faker(value)
        return self.faker.random_element(self.options)
