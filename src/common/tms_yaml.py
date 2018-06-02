from ruamel.yaml import YAML


class STREAM2STR():
    """ ruamel dumps data to a stream. We need dumping to a string.
        This class behaves partially as stream to dump to a string"""
    __str = ''

    def write(self, bytes_array):
        """ Stream write function. Here it dumps incoming bytes to string"""
        self.__str += bytes_array.decode("utf-8")

    def get_string(self):
        """ Returns string converted from stream """
        return self.__str


def yaml2py(yaml_str):
    """Function to convert yaml formatted string to python dict"""
    yaml = YAML(typ='safe', pure=True)
    return yaml.load(yaml_str)


def py2yaml(obj):
    """Function to convert python object to yaml formatted string"""
    str_stream = STREAM2STR()
    yaml = YAML(typ='safe', pure=True)
    yaml.default_flow_style = False
    yaml.dump(obj, str_stream)
    return str_stream.get_string()
