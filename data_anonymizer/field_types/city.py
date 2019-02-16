from data_anonymizer.field_types import BaseFieldType


class City(BaseFieldType):
    def generate_obfuscated_value(self, value):
        self.seed_faker(value)
        return self.faker.city()
