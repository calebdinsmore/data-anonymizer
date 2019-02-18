from .city import City
from .custom import Custom
from .custom_address import CustomAddress
from .custom_name import CustomName
from .date_time import DateTimeField
from .first_name import FirstName
from .float_range import FloatRange
from .full_address import FullAddress
from .full_name import FullName
from .int_range import IntRange
from .last_name import LastName
from .options import Options
from .ssn import SSN
from .street_address import StreetAddress
from .zip import Zip


class FieldTypeFactory:
    ACCEPTED_TYPES = {
        'city': City,
        'custom': Custom,
        'customaddress': CustomAddress,
        'customname': CustomName,
        'datetime': DateTimeField,
        'firstname': FirstName,
        'floatrange': FloatRange,
        'fulladdress': FullAddress,
        'fullname': FullName,
        'intrange': IntRange,
        'lastname': LastName,
        'options': Options,
        'ssn': SSN,
        'streetaddress': StreetAddress,
        'zip': Zip,
    }

    @staticmethod
    def get_type(type_config):
        if not isinstance(type_config, dict):
            raise ValueError('Column type configuration must be a dictionary')
        if not type_config.get('type'):
            raise ValueError('Must supply field type for column configuration')
        type_value = type_config['type'].lower()
        field_type_class = FieldTypeFactory.ACCEPTED_TYPES.get(type_value)
        if field_type_class is None:
            raise ValueError('Field type ' + type_config['type'] + ' not accepted.')
        return field_type_class(type_config)
