import os

def list_files(directory: str, extenstion: str="") -> list:
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extenstion):
                file_list.append(os.path.join(root, file))
    return file_list


def try_float(value):
    try:
        return float(value)
    except ValueError:
        return value


def try_detuple(t: tuple):
    return t[0] if len(t) == 1 else t


def csv_reader(filename: str, line_single: bool=True) -> tuple:
    output_list = []
    with open(filename) as f:
        for line in f.readlines():
            add = tuple(map(try_float, line.rstrip("\n").split(",")))
            add = try_detuple(add) if line_single else add
            output_list.append(add)
    return tuple(output_list)


def iter_add(x, y) -> list:
    r = []
    for i in range(0, len(x)):
        r.append(x[i] + y[i])
    return r
