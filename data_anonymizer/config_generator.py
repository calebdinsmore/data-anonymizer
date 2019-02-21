import csv
import dateutil.parser as date_parser
from .config import Config
import logging


def generate_yaml_config(data_file, has_header, delimiter):
    data_dict = build_data_dictionary(data_file, has_header, delimiter)
    new_config = Config(delimiter=delimiter)
    for column in data_dict:
        column_config = get_best_column_config_for_column(data_dict[column])
        if column_config is None:
            continue
        new_config.add_column_config(column, column_config)
    config_file_name = 'generated-{}-config.yml'.format(data_file)
    new_config.save_config(save_name=config_file_name)


def get_logger():
    return logging.getLogger('config_generator')


def build_data_dictionary(data_file, has_header, delimiter):
    """
    Builds a dictionary where the keys are the columns in the CSV, and the values are lists of that column's values
    :param data_file: str
    :param has_header: boolean
    :param delimiter: str
    :return: dict
    """
    data_dict = {}
    with open(data_file) as in_file:
        column_names = []
        if has_header:
            reader = csv.DictReader(in_file, delimiter=delimiter)
            column_names = reader.fieldnames
            for column in column_names:
                data_dict[column] = []
        else:
            reader = csv.reader(in_file, delimiter=delimiter)
        for row in reader:
            if not column_names:
                column_names = list(range(len(row)))
                for column in column_names:
                    data_dict[column] = []
            for column in column_names:
                if row[column]:
                    data_dict[column].append(row[column])
    return data_dict


def get_best_column_config_for_column(column_values):
    if len(column_values) == 0:
        return
    column_config = get_date_time_config_if_dates_found(column_values)
    if column_config:
        return column_config
    column_config = get_options_config_if_fewer_than_five_hundred(column_values)
    if column_config:
        return column_config
    return get_default_custom_column_config(column_values)


def get_date_time_config_if_dates_found(column_values):
    """
    If the values in the column look like dates, return a datetime column configuration
    :param column_values:
    :return:
    """
    sample_value: str = column_values.pop(0)
    while sample_value is None and len(column_values) > 0:
        sample_value = column_values.pop(0)
    if sample_value is None:
        return
    match = get_matched_date(sample_value)
    if match is not None:
        column_values.append(sample_value)
        min_date = None
        max_date = None
        for value in column_values:
            matched_date = get_matched_date(value)
            if matched_date is not None:
                if min_date is None or matched_date < min_date:
                    min_date = matched_date
                if max_date is None or matched_date > max_date:
                    max_date = matched_date
        return {
            'type': 'datetime',
            'format': '%Y-%m-%d',
            'range_start_date': min_date.strftime('%Y-%m-%d'),
            'range_end_date': max_date.strftime('%Y-%m-%d'),
        }


def get_matched_date(value):
    if len(value) < 6:
        return
    try:
        return date_parser.parse(value)
    except ValueError:
        return
    except OverflowError:
        get_logger().debug('Got overflow error trying to match %s', value)


def get_options_config_if_fewer_than_five_hundred(column_values):
    """
    If there are fewer than 500 unique values for a column, return an Options configuration dictionary
    :param column_values:
    :return:
    """
    unique_dict = {}
    for value in column_values:
        unique_dict[value] = True
    uniques = list(unique_dict.keys())
    if len(unique_dict.values()) < 500:
        return {
            'type': 'options',
            'options': uniques
        }


def get_default_custom_column_config(column_values):
    sample_value: str = column_values.pop(0)
    while sample_value is None and len(column_values) > 0:
        sample_value = column_values.pop(0)
    if sample_value is None:
        format_string = '????'
    else:
        format_string = ''
        for char in sample_value:
            if char.isalpha():
                format_string += '?'
            elif char.isnumeric():
                format_string += '#'
            else:
                format_string += char
    return {
        'type': 'custom',
        'format': format_string
    }
