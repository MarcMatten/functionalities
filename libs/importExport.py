import json
import csv
import numpy as np


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)


# def saveCSV(data, path):
#
#
# def loadCSV(path, *args):
#
#     if len(args) > 0:
#         header =
#
#     self.db.__setattr__('map', [])
#     self.db.__setattr__('x', [])
#     self.db.__setattr__('y', [])
#     self.db.__setattr__('dist', [])
#     self.db.__setattr__('time', [])
#
#     with open(path) as csv_file:
#
#         csv_reader = csv.reader(csv_file)
#
#         for line in csv_reader:
#             self.db.dist.append(float(line[0]))
#             self.db.x.append(float(line[1]))
#             self.db.y.append(float(line[2]))
#             self.db.time.append(float(line[3]))
#
#             self.db.map.append([float(line[1]), float(line[2])


def loadJson(path: str):
    with open(path) as jsonFile:
        data = json.loads(jsonFile.read())

    return data


def saveJson(data: dict, path: str):

    keys = list(data.keys())

    dataOut = {}

    for i in range(0, len(keys)):
        dataOut[keys[i]] = data[keys[i]]

    with open(path, 'w') as outfile:
        json.dump(dataOut, outfile, indent=4, sort_keys=True, cls=NumpyArrayEncoder)