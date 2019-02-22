def apply_formatting_options(func):
    def wrapper(self, *args, **kwargs):
        type_config_dict = getattr(self, 'type_config_dict')
        supplied_key = args[0]
        supplied_value = args[1]
        anonymized_value = func(self, supplied_key, supplied_value)
        if type_config_dict.get('upper'):
            anonymized_value = anonymized_value.upper()
        if type_config_dict.get('lower'):
            anonymized_value = anonymized_value.lower()
        return anonymized_value
    return wrapper
