import json
import sys
import os.path

from life import Life

class ArgumentException(Exception): pass

def read_pattern_file(filename):
    return json.loads(open(filename, 'r').read())

def write_pattern_file(filename, game):
    output = open(filename, "w")
    cell_collection = {'cells':[]}
    for cell in game.get_state():
        cell_collection['cells'].append( {'y':cell[0], 'x':cell[1]} )
    output.write(json.dumps(cell_collection))
    output.close()

def parse_args():
    args = sys.argv
    if len(args) > 2:
        raise ArgumentException('Expected 1 argument, {x} given'.format(x=len(args)-1))
    if len(args) == 2:
        if not os.path.isfile(args[1]):
            raise IOError(args[1]) #pass up file name
        return read_pattern_file(args[1])["cells"]
    else:
        return None
