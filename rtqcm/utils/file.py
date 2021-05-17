import os


def get_dir_from_name(filename):
    dir = os.path.dirname(filename)
    return dir


def get_simulation_filename_from_name(filename):
    separator = '_'
    name = os.path.basename(filename).split(separator)[1:]
    name = separator.join(name)
    separator = '.'
    name = os.path.basename(filename).split(separator)[0] + '_simulation'
    return name
