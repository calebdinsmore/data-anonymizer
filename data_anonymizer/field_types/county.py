from data_anonymizer.field_types import BaseFieldType
from .decorators import apply_formatting_options


class County(BaseFieldType):
    @apply_formatting_options
    def generate_obfuscated_value(self, key, value):
        self.seed_faker(key, value)
        return '{} County'.format(self.faker.last_name())
