import json
import sys
import os.path

from life import Life

class ArgumentException(Exception): pass

def read_pattern_file(filename):
    return json.loads(open(filename, 'r').read())

def write_pattern_file(filename, game):
    output = open(filename, "w")
    js = json.dumps(game.get_state())
    output.write(js)
    output.close()

def parse_args():
    args = sys.argv
    if len(args) > 2:
        raise ArgumentException('Expected 1 argument, {x} given'.format(x=len(args)-1))
    if len(args) == 2:
        if not os.path.isfile(args[1]):
            raise IOError('File \'{x}\' not found'.format(x=args[1]))
        return read_pattern_file(args[1])["cells"]
    else:
        return None