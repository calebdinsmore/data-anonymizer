from .city import City
from .custom import Custom
from .datetime import DateTime
from .first_name import FirstName
from .full_address import FullAddress
from .full_name import FullName
from .last_name import LastName
from .options import Options
from .ssn import SSN
from .street_address import StreetAddress
from .zip import Zip


class FieldTypeFactory:

    @staticmethod
    def get_type(type_config):
        if isinstance(type_config, list):
            return Options(type_config)
        if not isinstance(type_config, dict):
            raise ValueError('Column type configuration must be a list or dictionary')
        if not type_config.get('type'):
            raise ValueError('Must supply field type for column configuration')
        type_value = type_config['type'].lower()
        if type_value == 'city':
            return City()
        if type_value == 'custom':
            return Custom(type_config)
        if type_value == 'datetime':
            return DateTime(type_config)
        if type_value == 'firstname':
            return FirstName()
        if type_value == 'fulladdress':
            return FullAddress()
        if type_value == 'fullname':
            return FullName()
        if type_value == 'lastname':
            return LastName()
        if type_value == 'ssn':
            return SSN()
        if type_value == 'streetaddress':
            return StreetAddress()
        if type_value == 'zip':
            return Zip()
        raise ValueError(f"Field type {type_config['type']} not accepted.")
