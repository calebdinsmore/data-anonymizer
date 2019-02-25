from .city import City
from .custom import Custom
from .custom_address import CustomAddress
from .custom_name import CustomName
from .date_time import DateTimeField
from .email_address import EmailAddress
from .first_name import FirstName
from .float_range import FloatRange
from .full_address import FullAddress
from .full_name import FullName
from .int_range import IntRange
from .last_name import LastName
from .normal_int import NormalInt
from .options import Options
from .safe_harbor_age import SafeHarborAge
from .ssn import SSN
from .street_address import StreetAddress
from .zip import Zip


class FieldTypeFactory:
    ACCEPTED_TYPES = {
        'city': City,
        'custom': Custom,
        'custom_address': CustomAddress,
        'custom_name': CustomName,
        'datetime': DateTimeField,
        'email_address': EmailAddress,
        'first_name': FirstName,
        'float_range': FloatRange,
        'full_address': FullAddress,
        'full_name': FullName,
        'int_range': IntRange,
        'last_name': LastName,
        'normal_int': NormalInt,
        'options': Options,
        'safe_harbor_age': SafeHarborAge,
        'ssn': SSN,
        'street_address': StreetAddress,
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
