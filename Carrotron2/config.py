from yaml import load

try:
    from yaml import CLoader as Loader  # If its there, take advantage of the faster LibYAML loader
except ImportError:
    from yaml import Loader  # No LibYAML, use pure


def load_yaml(str_or_buffer):
    """
    Load a yaml file or string and convert to dict
    """
    return load(str_or_buffer, Loader=Loader)


def load_yaml_from_file(filename):
    """
    Loads an environment file from file system
    """
    return load_yaml(open(filename))

def load_robot_config(filename):
    yaml = load_yaml_from_file(filename)

    r = Robot()


    print(yaml)

if __name__ == '__main__':
    load_robot_config('carrotron2.yaml')