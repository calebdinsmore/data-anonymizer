from . import BaseFieldType


class IntRange(BaseFieldType):
    def generate_obfuscated_value(self, key, value):
        self.seed_faker(key, value)
        if self.type_config_dict.get('start') is None:
            raise ValueError('"start" must be defined in config for IntRange column types.')
        if self.type_config_dict.get('end') is None:
            raise ValueError('"end" must be defined in config for IntRange column types.')
        start = int(self.type_config_dict.get('start'))
        end = int(self.type_config_dict.get('end'))
        return self.faker.random_int(start, end)
