import os


def read_env_file(env_file):
    with open(env_file, 'r') as fh:
        vars_dict = {
            tuple(line.split('=')) for line in fh.readlines() if not line.startswith('#')
        }
    os.environ.update(vars_dict)
    return vars_dict


def get_env(name, default=None):
    return os.getenv(name, default)
