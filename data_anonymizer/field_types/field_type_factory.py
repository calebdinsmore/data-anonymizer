from .city import City
from .custom import Custom
from .date_time import DateTimeField
from .first_name import FirstName
from .full_address import FullAddress
from .full_name import FullName
from .last_name import LastName
from .options import Options
from .ssn import SSN
from .street_address import StreetAddress
from .zip import Zip


class FieldTypeFactory:
    ACCEPTED_TYPES = {
        'city': City,
        'custom': Custom,
        'datetime': DateTimeField,
        'firstname': FirstName,
        'fulladdress': FullAddress,
        'fullname': FullName,
        'lastname': LastName,
        'options': Options,
        'ssn': SSN,
        'streetaddress': StreetAddress,
        'zip': Zip,
    }

    @staticmethod
    def get_type(type_config):
        if not isinstance(type_config, dict):
            raise ValueError('Column type configuration must be a list or dictionary')
        if not type_config.get('type'):
            raise ValueError('Must supply field type for column configuration')
        type_value = type_config['type'].lower()
        field_type_class = FieldTypeFactory.ACCEPTED_TYPES.get(type_value)
        if field_type_class is None:
            raise ValueError('Field type ' + type_config['type'] + ' not accepted.')
        return field_type_class(type_config)
