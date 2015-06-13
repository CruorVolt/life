import curses

class CellOutOfBounds(Exception): pass

class Life:

    def __init__(self, size, cells=None):
        assert len(size) == 2, "size should be a 2-tuple in (y,x) format"
        self.__size_y = size[0]
        self.__size_x = size[1]
        self.__live_cells = []
        if cells is not None:
            try:
                for cell in self.center(cells):
                    self.add_cell(cell)
            except CellOutOfBounds: raise

    def center(self, cell_dicts):
	'''
	Center the cells in cell_dicts to the middle
	of self's vertical/horizontal ranges.

	cell_dicts is of the form [ {'x'= #, 'y' = #}, ... ]
	'''

        x_list, y_list = [], []
        for pair_dict in cell_dicts:
            y_list.append(pair_dict['y'])
            x_list.append(pair_dict['x'])
        min_y, max_y  = min(y_list), max(y_list)
        min_x, max_x  = min(x_list), max(x_list)
        center_y, center_x = (max_y+min_y)//2, (max_x+min_x)//2
        shift_y = self.__size_y //2 - center_y
        shift_x = self.__size_x //2 - center_x
        for cell in zip(y_list, x_list):
            yield (cell[0] + shift_y, cell[1] + shift_x)

    def toggle_cell(self, cell):
        '''Toggle the state of the specified cell in this generation'''
        assert len(cell) == 2, "cell should be a 2-tuple coordinate pair (y,x)"
        if self.has_cell(cell):
            self.kill_cell(cell)
            return True
        else:
            self.add_cell(cell)
            return False

    def in_game(self, cell):
        '''Is the specified cell within the bounds of the game?'''
        y,x = cell #curses-style coordinate definitions
        return y >= 0 and x >= 0 and y <= self.__size_y and x <= self.__size_x

    def set_state(self, state):
        self.__live_cells = state

    def get_state(self):
        return self.__live_cells

    def add_cell(self, cell):
        '''Add the specified cell to this generation'''
        assert len(cell) == 2, "cell should be a 2-tuple coordinate pair (y,x)"
        if not self.in_game(cell): raise CellOutOfBounds
        self.__live_cells.append(cell)

    def kill_cell(self, cell):
        '''Remove the specified cell from this generation'''
        assert len(cell) == 2, "cell should be a 2-tuple coordinate pair (y,x)"
        self.__live_cells.remove(cell)

    def has_cell(self, cell):
        '''The cell is currently live in this game'''
        assert len(cell) == 2, "cell should be a 2-tuple coordinate pair (y,x)"
        return True if cell in self.__live_cells else False

    def cell_count(self):
        '''How many cells this generation has'''
        return len(self.__live_cells)

    def tick(self):
        '''Advance the game by one generation'''

        next_state = []
        dead_neighbors = {}
        for live in self.__live_cells:
            live_neighbors = 0
            for neighbor in self.get_neighbors(live):
                if (self.has_cell(neighbor)):
                    live_neighbors += 1
                else:
                    if not neighbor in dead_neighbors:
                        dead_neighbors[neighbor] = 1
                    else:
                        dead_neighbors[neighbor] += 1
            if live_neighbors in [2,3]: #This cell survives
                next_state.append(live)
        for key in dead_neighbors.keys():
            if dead_neighbors[key] == 3: #This cell is born
                next_state.append(key)
        self.set_state(next_state)
                    
    def get_neighbors(self, cell):
        '''Return list of 2-tuples representing the 8 neighboring cells'''
        neighbors = []
        for y in [cell[0] - 1, cell[0], cell[0] + 1]:
            for x in [cell[1] - 1, cell[1], cell[1] + 1]:
                if (y,x) != cell and self.in_game(cell):
                    neighbors.append((y,x)) 
        return neighbors
