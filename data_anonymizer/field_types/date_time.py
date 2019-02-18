from datetime import datetime
from . import BaseFieldType
from .decorators import apply_formatting_options


class DateTimeField(BaseFieldType):
    def __init__(self, type_config_dict):
        super().__init__(type_config_dict)
        format_string = type_config_dict.get('format')
        range_start_date = type_config_dict.get('range_start_date')
        range_end_date = type_config_dict.get('range_end_date')
        if not format_string or not isinstance(format_string, str):
            raise ValueError('DateTime field types must have a format defined of type string')
        self.format_string = format_string
        if range_start_date is None:
            range_start_date = datetime.strptime('01/01/1800', '%m/%d/%Y')
        else:
            range_start_date = datetime.strptime(range_start_date, format_string)
        if range_end_date is None:
            range_end_date = datetime.strptime('01/01/2018', '%m/%d/%Y')
        else:
            range_end_date = datetime.strptime(range_end_date, format_string)
        self.range_start_date = range_start_date
        self.range_end_date = range_end_date

    @apply_formatting_options
    def generate_obfuscated_value(self, value):
        self.seed_faker(value)
        generated_date = self.faker.date_time_between_dates(self.range_start_date, self.range_end_date)
        return generated_date.strftime(self.format_string)
