import yaml


class Config:
    def __init__(self, yaml_path):
        with open(yaml_path) as config_file:
            self.config_dict = yaml.load(config_file)
        self.secret_key = 'my-secret-key1'
        if self.secret_key is None:
            raise SecretKeyNotSetException

    @property
    def columns_to_obfuscate(self):
        return self.config_dict.get('columns_to_obfuscate')


class SecretKeyNotSetException(Exception):
    pass


# print(ObfuscationConfiguration('example-conf.yml').columns_to_obfuscate)
