from . import BaseFieldType


class Zip(BaseFieldType):
    RESTRICTED_ZIPS = [
        '036',
        '692',
        '878',
        '059',
        '790',
        '879',
        '063',
        '821',
        '884',
        '102',
        '823',
        '890',
        '203',
        '830',
        '893',
        '556',
        '831',
    ]

    def __generate_value_from_mask(self, mask, value):
        generated_value = ''
        mask = str(mask)
        value = str(value)
        # Ensure that restricted ZIPs don't ever get preserved.
        if len(value) > 3 and value[:3] in Zip.RESTRICTED_ZIPS:
            value = '000' + value[3:]
        if len(mask) != 5:
            raise ValueError('Zip field mask must be of length 5')
        for char_idx in range(len(mask)):
            char = mask[char_idx]
            if not char.isdigit() or (int(char) != 0 and int(char) != 1):
                raise ValueError('Mask must consist of 0s and 1s')
            if int(char) == 0:
                generated_value += str(self.faker.random_int(1, 9))
            else:
                try:
                    generated_value += value[char_idx]
                except IndexError:
                    return generated_value
        return generated_value

    def generate_obfuscated_value(self, key, value):
        self.seed_faker(key, value)
        mask = self.type_config_dict.get('mask')
        if mask is not None:
            return self.__generate_value_from_mask(mask, value)
        return self.faker.postcode()
