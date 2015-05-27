import curses

class Life:

    def __init__(self, size):
        assert len(size) == 2, "size should be a 2-tuple in (y,x) format"
        self.__size_y = size[0]
        self.__size_x = size[1]
        self.__live_cells = []

    def toggle_cell(self, cell):
        assert len(cell) == 2, "cell should be a 2-tuple coordinate pair (y,x)"
        if self.has_cell(cell):
            self.kill_cell(cell)
            return True
        else:
            self.add_cell(cell)
            return False

    def add_cell(self, cell):
        assert len(cell) == 2, "cell should be a 2-tuple coordinate pair (y,x)"
        self.__live_cells.append(cell)

    def kill_cell(self, cell):
        assert len(cell) == 2, "cell should be a 2-tuple coordinate pair (y,x)"
        self.__live_cells.remove(cell)

    def has_cell(self, cell):
        assert len(cell) == 2, "cell should be a 2-tuple coordinate pair (y,x)"
        return True if cell in self.__live_cells else False

    def cell_count(self):
        return len(self.__live_cells)


    def step(self):
        for live in self.__live_cells:
            for neighbor in get_neighbors(live):
    
    def get_neighbors(cell):
        pass
