class Life:

    def __init__(self, size):
        self.size_y = size[0]
        self.size_x = size[1]
        self.live_cells = []

    def toggle_cell(loc):
        kill_cell(loc) if has_cell(loc) else add_cell(loc)

    def add_cell(loc):
        self.live_cells.append(loc)

    def kill_cell(loc):
        self.live_cells.remove(loc)

    def has_cell(loc):
        return True if loc in self.live_cells else False
