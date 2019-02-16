from . import BaseFieldType


class SSN(BaseFieldType):
    def generate_obfuscated_value(self, value):
        self.seed_faker(value)
        return self.faker.ssn()
