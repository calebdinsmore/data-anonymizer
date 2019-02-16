import csv
from data_anonymizer.config import Config
from data_anonymizer.field_types.field_type_factory import FieldTypeFactory
from timeit import default_timer as timer


def anonymize():
    config = Config('example-conf.yml')
    with open('applcnt-insite06-20181206.csv') as in_file:
        with open('applcnt-obfuscated.csv', 'w') as out_file:
            reader = csv.DictReader(in_file)
            writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                for column_name in config.columns_to_obfuscate:
                    if column_name not in row:
                        raise ValueError(f'{column_name} not found in CSV.')
                    type_config_dict = config.columns_to_obfuscate[column_name]
                    field_type = FieldTypeFactory.get_type(type_config_dict)
                    if field_type is not None and row[column_name] is not None:
                        row[column_name] = field_type.generate_obfuscated_value(config.secret_key + row[column_name])
                writer.writerow(row)

