from . import BaseFieldType


class Options(BaseFieldType):
    def __init__(self, options):
        super().__init__()
        self.options = options

    def generate_obfuscated_value(self, value):
        self.seed_faker(value)
        return self.faker.random_element(self.options)
