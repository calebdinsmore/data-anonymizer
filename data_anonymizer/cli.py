#!/usr/bin/env python3

import argparse
import csv
import os
from data_anonymizer.config import Config
from data_anonymizer.field_types.field_type_factory import FieldTypeFactory
from data_anonymizer.config_generator import generate_yaml_config


def exit_with_message(message, code):
    print(message)
    exit(code)


def anonymize(config_file, in_filename, out_filename):
    config = Config(config_file)
    with open(in_filename) as in_file:
        with open(out_filename, 'w') as out_file:
            reader = csv.DictReader(in_file)
            writer = csv.DictWriter(out_file, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                for column_name in config.columns_to_obfuscate:
                    if column_name not in row:
                        raise ValueError(column_name + ' not found in CSV.')
                    type_config_dict = config.columns_to_obfuscate[column_name]
                    field_type = FieldTypeFactory.get_type(type_config_dict)
                    if field_type is not None and row[column_name] is not None:
                        row[column_name] = field_type.generate_obfuscated_value(config.secret_key + row[column_name])
                writer.writerow(row)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='File to anonymize')
    parser.add_argument('--config', '-c', help='YAML config file (required) specifying how to anonymize the data.'
                                               ' Generate one with the --generate-config flag')
    parser.add_argument('--generate-config', '-g', action='store_true', help='Generate config file based on CSV provided')
    parser.add_argument('--has-header',
                        action='store_true',
                        default=True,
                        help='Specify if a header is present. Defaults to true.')
    parser.add_argument('--keygen', '-k', action='store_true', help='Generates a key file to use.')
    parser.add_argument('--outfile', '-o', help='Name/path of file to output (defaults to anonymized-INFILE_NAME')

    args = parser.parse_args()
    if not os.path.isfile(args.file):
        exit_with_message('No such file: ' + args.file, 1)
    if args.generate_config:
        generate_yaml_config(args.file, args.keygen, args.has_header)
        return
    if not args.outfile:
        outfile = 'anonymized-' + args.file
    else:
        outfile = args.outfile
    if not args.config:
        parser.print_help()
        exit_with_message('ERROR: Specify a YAML config file with --config.', 1)
    anonymize(args.config, args.file, outfile)
