from . import BaseFieldType


class FullAddress(BaseFieldType):
    def generate_obfuscated_value(self, value):
        self.seed_faker(value)
        return self.faker.address()
