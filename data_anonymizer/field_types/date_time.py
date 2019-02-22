import dateutil.parser as date_parser
from datetime import datetime
from . import BaseFieldType
from .decorators import apply_formatting_options


class DateTimeField(BaseFieldType):
    def __init__(self, type_config_dict):
        super().__init__(type_config_dict)
        format_string = type_config_dict.get('format')
        range_start_date = type_config_dict.get('range_start_date')
        range_end_date = type_config_dict.get('range_end_date')
        self.preserve_year = type_config_dict.get('preserve_year')
        self.safe_harbor = type_config_dict.get('safe_harbor')
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
    def generate_obfuscated_value(self, key, value):
        self.seed_faker(key, value)
        generated_date = self.faker.date_time_between_dates(self.range_start_date, self.range_end_date)
        if self.preserve_year:
            try:
                if generated_date.month == 2 and generated_date.day == 29:
                    generated_date = generated_date.replace(month=3)
                value_year = date_parser.parse(value).year
                generated_date = generated_date.replace(year=value_year)
            except ValueError:
                self.get_logger().warning('Could not parse year from %s. Unable to preserve year.', value)
        if self.safe_harbor and abs(generated_date.year - datetime.today().year) >= 90:
            year_delta_150 = datetime.today().year - 150
            generated_date = generated_date.replace(year=year_delta_150)
        return generated_date.strftime(self.format_string)
