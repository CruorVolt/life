from curses import wrapper
from life import *

cell_list = {} #curses window objects returned by newwin()
game = None

def main(screen): 

    global cell_list,game

    curses.start_color() 

    curses.curs_set(0) #never visible cursor

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) #bottom frame
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK) #dead cell
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN) #new cell
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_RED) #cursor
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN) #border

    screen.bkgd(curses.color_pair(6)) 
    screen.refresh() 

    y,x = screen.getmaxyx()

    for col in range(1,y-2):
        for row in range(1, x-2):
            new_win = curses.newwin(1,1,col,row)
            new_win.bkgd(curses.color_pair(2))
            new_win.refresh() #or they won't fill the background right
            cell_list[(col,row)] = new_win

    current_cursor = move_cursor(screen, None, (y//2, x//2))

    game = Life( (y-2,x-2) )

    borderwin = curses.newwin(1, x, y-1, 0)
    borderwin.bkgd(curses.color_pair(1))
    borderwin.refresh() 

    while 1:
        c = screen.getch()
        cursor_y, cursor_x = current_cursor
        if c == ord('q') or c == 27:
            exit()
        elif c in [curses.KEY_LEFT, ord('a'), ord('h')]:
            current_cursor = move_cursor(screen, current_cursor, (cursor_y, cursor_x - 1))
        elif c in [curses.KEY_RIGHT, ord('d'), ord('l')]:
            current_cursor = move_cursor(screen, current_cursor, (cursor_y, cursor_x + 1))
        elif c in [curses.KEY_UP, ord('w'), ord('k')]:
            current_cursor = move_cursor(screen, current_cursor, (cursor_y - 1, cursor_x))
        elif c in [curses.KEY_DOWN, ord('s'), ord('j')]:
            current_cursor = move_cursor(screen, current_cursor, (cursor_y + 1, cursor_x))
        elif c == 10 or c == 32: #CR and SPACE
            draw_cell((cursor_y, cursor_x))
        elif c == ord('i'):
            display_help(win)

        borderwin.addstr(0,0, "CY={y}".format(y=cursor_y))
        borderwin.addstr(0,10, "CX={x}".format(x=cursor_x))
        borderwin.addstr(0,20, "Cells: {cells}".format(cells=game.cell_count()))
        borderwin.refresh()

def move_cursor(window, current_cell, new_cell):
    '''Moves the cursor to the new location, respecting window edges.

    window is the curses window object with the cursor to be moved. 
    new_x and new_y are the desired x and y coordinates of the cursor.
    move_cursor will either modify the window to hav the cursor set at
    the new location or do nothing if the desired coordinates are outside
    the window's borders.
    '''

    global cell_list, game

    max_y, max_x = window.getmaxyx()
    new_y, new_x = new_cell
    if new_y >= 0 and new_x >= 0 and new_y <= max_y-1 and new_x < max_x:
        if current_cell:
            #if game.in_game
            cell_list[current_cell].bkgd(curses.color_pair(2))
            cell_list[current_cell].refresh()
        cell_list[new_cell].bkgd(curses.color_pair(4))
        cell_list[new_cell].refresh()
        current_cell = new_cell
    return current_cell

def draw_cell(coords):
    global cell_list, game
    cell_exists = game.toggle_cell(coords)
    if cell_exists:
        delete_cell(coords)
    else:
    	add_cell(coords)

def delete_cell(coords):
    global cell_list, game
    pass

def add_cell(coords):
    global cell_list, game
    window = curses.newwin(1, 2, coords[0]+1, coords[1]+1) 
    cell_list[coords].bkgd(curses.color_pair(3))
    cell_list[coords].refresh()

def display_help(window):
    size = window.getmaxyx()
    message = " ".join(["        CONWAY'S  GAME  OF  LIFE\n\n",
        "Move the cursor with **** WASD or KJHL\n\n",
        "Paint/delete cells with SPACE or ENTER"])

    help_pane = curses.newwin(7, 40, size[0]//2-3, size[1]//2-20) 
    help_pane.bkgd(green) 

    help_pane.addstr(1,0,message)
    help_pane.addch(3,22,curses.ACS_UARROW)
    help_pane.addch(3,23,curses.ACS_DARROW)
    help_pane.addch(3,24,curses.ACS_LARROW)
    help_pane.addch(3,25,curses.ACS_RARROW)

    help_pane.getch()
    help_pane.erase

wrapper(main) 
