# Data Anonymizer

Data Anonymizer is a tool that helps you anonymize data you're working with and building reports on.

## Installation

`pip3 install --user data-anonymizer`\*

\* Needs Python 3 to run at the moment.

## Usage

```
usage: data-anomymizer [-h] [--config CONFIG] [--delimiter DELIMITER]
                       [--generate-config] [--no-header] [--key-file KEY_FILE]
                       [--outfile OUTFILE]
                       file

positional arguments:
  file                  File to anonymize

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        YAML config file (required) specifying how to
                        anonymize the data. Generate one with the --generate-
                        config flag
  --delimiter DELIMITER, -d DELIMITER
                        Specify delimiter the CSV uses (defaults to ",")
  --generate-config, -g
                        Generate config file based on CSV provided
  --no-header           Specify if a header is not present.
  --key-file KEY_FILE   Specify the file to get the key from.
  --outfile OUTFILE, -o OUTFILE
                        Name/path of file to output (defaults to anonymized-
                        INFILE_NAME
```

## How it works

This tool accepts three things:

- A key file
    - If one is not supplied, the tool generates one and saves it to `anonymizer.key` or uses it if it is present in the current working directory
- A config file (YAML)
    - You can generate one for your data using `--generate-config`
- A data set to anonymize (only accepts CSV at the moment)

The config file should specify how to anonymize the data in each of the CSV's columns. It should look something like this:

```yaml
delimiter: ','
columns_to_anonymize:
  FirstName:
    type: first_name
    upper: true
  SSN:
    type: ssn
  FullName:
    type: custom_name
    format: '$LAST, $FIRST $MI'
  DOB:
    type: datetime
    format: '%Y/%m/%d'
    range_start_date: '2000/01/01'
    range_end_date: '2010/01/01'
```

The config provides metadata on the kind of data within each column. In the example above, FirstName, SSN, FullName, and DOB are the literal column headers in the CSV.

The `type` attribute in the config refers to different defined field types that data-anonymizer recognizes. All defined field types are listed below.

### Generating anonymous values (and maintaining referential integrity)

`data-anonymizer` generates anonymous values using the [faker](https://github.com/joke2k/faker) library.

It's able to preserve the shape of the data and its referential integrity because of how it generates those values. It generates them like so:

- For every value in the data set:
    - Concatenate value to provided key (in key file)
    - Hash newly concatenated value
    - Seed `faker`'s random generator with the hash
    - Generate value for column
    
This means that for a given provided key, the same value will always be converted to the same anonymous value.

Say for instance that you are anonymizing `sensitive-file-A.csv` with the key `my-cool-key-1234`.

A value of `Robert California` in that file is anonymized to `John Smith`.

If you then anonymize `sensitive-file-B.csv`, and it contains a record with the value `Robert California`, **as long as you use the same key,** that record will also be anonymized to `John Smith`.

Because of this, the shape of the data is preserved, and any columns that contain things that are referenced in related tables are anonymized to the same value in those tables. This preserves referential integrity.

## Configuration Column Types

These are the different available types and the different attributes each recognizes. Each column type that produces output containing or potentially containing alphabetical characters also accepts the following attributes:

- `upper`
    - Set to `true` to uppercase the generated value for a given column
- `lower`
    - Set to `true` to lowercase the generated value for a given column

### city

Generates a random real-sounding city using `faker`'s city provider.

---

### custom

Generate a string with a custom format. This uses `faker`'s syntax for its `bothify` provider, which converts certain symbols into random letters or numbers, depending on the symbol.

**Special Attributes**
- `format`

Here are the special symbols the format attribute recognizes:

- '?' : Generates a random alphabetical character
- '#' : Generates a random number between 0 and 9
- '%' : Generates a random number between 1 and 9
- '!' : Generates a random number between 0 and 9 or an empty string
- '@' : Generates a random number between 1 and 9 or an empty string

Example configuration:
```yaml
ID:
  type: custom
  format: 'ID-??-##-%'
```

Could yield `ID-dF-03-5`

---

### custom_address

Generate address using custom `format` option

**Special Attributes**
- `format`

The format attribute for this type accepts special keywords and replaces them with generated values. It also accepts any of the special symbols the `custom` column configuration accepts.

The special symbols the `custom_address` `format` attribute recognizes are the following:

- `$STREET` : Generates a real-sounding street address (number + street name)
- `$CITY` : Generates a real-sounding city name
- `$ZIP` : Generates a valid zip code
- `$STATE_ABBR` - Selects a random abbreviated state among the 50 US states.
- `$STATE_FULL` - Selects a random spelled-out state among the 50 US states.

**Note:** if the `format` attribute is omitted, a full address is generated, including street, city, state, and zip.

Example configuration:
```yaml
HomeAddress:
  type: custom_address
  format: '$STREET, $CITY, blah $STATE_ABBR #?'
```

Could yield `2073 David Square, Nixonburgh, blah AL 5g`

---

### custom_name

Generate name using custom `format` option.

**Special Attributes**
- `format`

The format attribute for this type accepts special keywords and replaces them with generated values. It also accepts any of the special symbols the `custom` column configuration accepts.

The special symbols the `custom_name` `format` attribute recognizes are the following:

- `$FIRST` : Generates a real-sounding first name
- `$LAST` : Generates a real-sounding last name
- `$MI` : Generates an upper-cased initial

**Note:** if the `format` attribute is omitted, a full name is generated of form `$FIRST $LAST`

Example configuration:
```yaml
FullName:
  type: custom_name
  format: '$LAST, $FIRST $MI'
```

Could yield `Obrien, Michael F`

---

### datetime

Generate a datetime between two dates with a custom datetime format.

**Special Attributes**
- `format`
    - Desired format of the generated value (using Python datetime strptime syntax)
    - Required
- `range_start_date`
    - Desired start date in the range of dates to generate
    - Must be written according to the format specified in `format`
    - Defaults to: 1800/01/01
- `range_end_date`
    - Desired end date in the range of dates to generate
    - Must be written according to the format specified in `format`
    - Defaults to: 2018/01/01


Example configuration:
```yaml
DOB:
  type: datetime
  format: '%Y/%m/%d'
  range_start_date: '1950/01/01'
  range_end_date: '2019/01/01'
```

Could yield `1976/04/23`

---

### first_name

Generates a real-sounding first name using `faker`'s first_name provider.

---

### float_range

Generate a float between two numbers.

**Special Attributes**
- `start`
    - Desired start value
    - Required
- `end`
    - Desired end value
    - Required
- `precision`
    - Number of digits to round to


Example configuration:
```yaml
Cost:
  type: float_range
  start: 1
  end: 100
  precision: 2
```

Could yield `54.56`

---

### full_address

Generates a real-sounding full address.

---

### full_name

Generates a real-sounding full name.

---

### int_range

Generate an integer between two numbers.

**Special Attributes**
- `start`
    - Desired start value
    - Required
- `end`
    - Desired end value
    - Required


Example configuration:
```yaml
Total:
  type: int_range
  start: 0
  end: 1000
```

Could yield `435`

---

### last_name

Generates a real-sounding last name.

---

### options

Selects a value from a defined list of options.

**Special Attributes**
- `options`
    - A list of valid options to choose from.
    - Required

Example configuration:
```yaml
Sex:
  type: options
  options:
    - MALE
    - FEMALE
    - UNKNOWN
```

Could yield `FEMALE`

---

### ssn

Generate an SSN of form `###-##-####`.

---

### street_address

Generate a real-sounding street address.

---

### zip

Generate a valid-looking ZIP code.

---
