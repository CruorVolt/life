import json
import sys
import os.path

from life import Life


def read_pattern_file(filename):
    return json.loads(open(filename, 'r').read())


def write_pattern_file(filename, game):
    '''
    Write the current state of game to 
    the relative pathed fiel filename
    '''

    if len(filename) == 0:
        return False #indicate no file written
    output = open(filename, "w")
    cell_collection = {'cells':[]}
    for cell in game.get_state():
        cell_collection['cells'].append( {'y':cell[0], 'x':cell[1]} )
    output.write(json.dumps(cell_collection))
    output.close()
    return True


def parse_args():
    '''
    Pass the pattern in the specified file,
    '''

    args = sys.argv
    if len(args) > 2:
        raise ArgumentException('Expected 1 argument, {x} given'.format(x=len(args)-1))
    if len(args) == 2:
        if not os.path.isfile(args[1]):
            raise IOError(args[1]) #pass up file name
        return read_pattern_file(args[1])["cells"]
    else:
        return None
