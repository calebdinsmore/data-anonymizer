from . import BaseFieldType


class SafeHarborAge(BaseFieldType):
    def generate_obfuscated_value(self, key, value):
        if int(value) >= 90:
            return 150
        return value
