from . import BaseFieldType


class SSN(BaseFieldType):
    def generate_obfuscated_value(self, key, value):
        self.seed_faker(key, value)
        return self.faker.ssn()
