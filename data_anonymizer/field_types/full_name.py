from . import BaseFieldType


class FullName(BaseFieldType):
    def generate_obfuscated_value(self, value):
        self.seed_faker(value)
        return self.faker.name()
