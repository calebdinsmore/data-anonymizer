#!/usr/bin/env python3

import argparse
import csv
import os
import logging
from data_anonymizer.config import Config
from data_anonymizer.field_types.field_type_factory import FieldTypeFactory
from data_anonymizer.config_generator import generate_yaml_config


DEFAULT_KEY_FILE = 'anonymizer.key'


def anonymize(config, in_filename, out_filename, has_header):
    with open(in_filename) as in_file:
        with open(out_filename, 'w') as out_file:
            if has_header:
                reader = csv.DictReader(in_file, delimiter=config.delimiter)
                writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames, delimiter=config.delimiter)
                writer.writeheader()
            else:
                reader = csv.reader(in_file, delimiter=config.delimiter)
                writer = csv.writer(out_file, delimiter=config.delimiter)
            for row in reader:
                for column_name in config.columns_to_anonymize:
                    if column_name not in row and has_header:
                        raise ValueError(str(column_name) + ' not found in CSV.')
                    type_config_dict = config.columns_to_anonymize[column_name]
                    field_type = FieldTypeFactory.get_type(type_config_dict)
                    if field_type is not None and row[column_name] is not None and row[column_name] is not '':
                        row[column_name] = field_type.generate_obfuscated_value(config.secret_key, row[column_name])
                writer.writerow(row)


def keygen():
    import random
    import string
    with open(DEFAULT_KEY_FILE, 'w') as key_file:
        # Generate random alphanumeric key of length 15
        key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
        key_file.write(key)


def exit_with_message(message, code):
    print(message)
    exit(code)


def get_logger():
    return logging.getLogger('data-anonymizer')


def main():
    get_logger().setLevel(logging.WARNING)
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='File to anonymize')
    parser.add_argument('--config', '-c', help='YAML config file (required) specifying how to anonymize the data.'
                                               ' Generate one with the --generate-config flag')
    parser.add_argument('--delimiter', '-d', default=',', help='Specify delimiter the CSV uses (defaults to ",")')
    parser.add_argument('--generate-config', '-g', action='store_true', help='Generate config file based on CSV provided')
    parser.add_argument('--no-header',
                        action='store_true',
                        help='Specify if a header is not present.')
    parser.add_argument('--key-file', '-k', help='Specify the file to get the key from.')
    parser.add_argument('--outfile', '-o', help='Name/path of file to output (defaults to anonymized-INFILE_NAME')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show verbose debug info')

    args = parser.parse_args()

    if args.verbose:
        get_logger().setLevel(logging.DEBUG)

    has_header = not args.no_header
    if not os.path.isfile(args.file):
        exit_with_message('No such file: ' + args.file, 1)
    if args.generate_config:
        generate_yaml_config(args.file, has_header, args.delimiter)
        return
    if not args.config:
        parser.print_help()
        exit_with_message('ERROR: Specify a YAML config file with --config.', 1)
    outfile = args.outfile
    key_file = args.key_file
    if not args.outfile:
        outfile = 'anonymized-' + args.file
    if not args.key_file: 
        if not os.path.isfile(DEFAULT_KEY_FILE):
            get_logger().warning('Key file not specified. Generating and using %s file', DEFAULT_KEY_FILE)
            get_logger().warning('Make sure to use this key file when anonymizing other data sets.')
            keygen()
        key_file = DEFAULT_KEY_FILE
    config = Config(args.config, key_file, delimiter=args.delimiter)
    anonymize(config, args.file, outfile, has_header)
