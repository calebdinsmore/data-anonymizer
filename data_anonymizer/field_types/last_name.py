from . import BaseFieldType


class LastName(BaseFieldType):
    def generate_obfuscated_value(self, value):
        self.seed_faker(value)
        return self.faker.last_name()
