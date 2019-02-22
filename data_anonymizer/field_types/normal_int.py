from . import BaseFieldType


class NormalInt(BaseFieldType):
    def generate_obfuscated_value(self, key, value):
        self.seed_faker(key, value)
        if self.type_config_dict.get('mean') is None:
            raise ValueError('"mean" must be defined in config for normal_int column types.')
        if self.type_config_dict.get('st_dev') is None:
            raise ValueError('"st_dev" must be defined in config for normal_int column types.')
        mean = float(self.type_config_dict.get('mean'))
        st_dev = float(self.type_config_dict.get('st_dev'))
        return abs(int(self.faker.random.normalvariate(mean, st_dev)))
