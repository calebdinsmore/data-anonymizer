from . import BaseFieldType
from .decorators import apply_formatting_options


class LastName(BaseFieldType):
    @apply_formatting_options
    def generate_obfuscated_value(self, value):
        self.seed_faker(value)
        return self.faker.last_name()
