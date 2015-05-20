import curses.wrapper
from life import *

def main(screen): 

    curses.start_color() 

    curses.curs_set(2) #always visible cursor

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLUE)
    screen.bkgd(curses.color_pair(2)) 
    screen.refresh() 

    y,x = screen.getmaxyx()
    win = curses.newwin(y-2, x-2, 1, 1) 

    game = Life( (y-2,x-2) )

    win.bkgd(curses.color_pair(0)) 

    borderwin = curses.newwin(1, x, y-1, 0)
    borderwin.bkgd(curses.color_pair(1))

    move_cursor(win, y//2, x//2)
    borderwin.refresh() 
    win.refresh() 

    cell_list = []

    while 1:
        c = screen.getch()
        cursor = win.getyx()
        cursor_y = cursor[0]
        cursor_x = cursor[1]
        if c == ord('q') or c == 27:
            exit()
        elif c in [curses.KEY_LEFT, ord('a'), ord('h')]:
            move_cursor(win, cursor_y, cursor_x - 1)
        elif c in [curses.KEY_RIGHT, ord('d'), ord('l')]:
            move_cursor(win, cursor_y, cursor_x + 1)
        elif c in [curses.KEY_UP, ord('w'), ord('k')]:
            move_cursor(win, cursor_y - 1, cursor_x)
        elif c in [curses.KEY_DOWN, ord('s'), ord('j')]:
            move_cursor(win, cursor_y + 1, cursor_x)
        elif c == 10 or c == 32: #CR and SPACE
            draw_cell((cursor_y, cursor_x), cell_list, game)
        elif c == ord('i'):
            display_help(win)
            curses.curs_set(2)
            win.redrawwin()
            win.touchwin()

        borderwin.addstr(0,0, "CY={y}".format(y=cursor_y))
        borderwin.addstr(0,10, "CX={x}".format(x=cursor_x))
        borderwin.addstr(0,20, "Cells: {cells}".format(cells=game.cell_count()))
        borderwin.refresh()
	for cell in cell_list: 
            cell.redrawwin()
            cell.refresh()
        win.refresh()

def move_cursor(window, new_y, new_x):
    '''Moves the cursor to the new location, respecting window edges.

    window is the curses window object with the cursor to be moved. 
    new_x and new_y are the desired x and y coordinates of the cursor.
    move_cursor will either modify the window to hav the cursor set at
    the new location or do nothing if the desired coordinates are outside
    the window's borders.
    '''

    max_y, max_x = window.getmaxyx()
    if new_y >= 0 and new_x >= 0 and new_y <= max_y-1 and new_x < max_x:
        window.move(new_y, new_x)

def draw_cell(coords, cell_list, game):
    cell_exists = game.toggle_cell(coords)
    if cell_exists:
        delete_cell(coords, cell_list, game) #TODO: implement
    else:
    	add_cell(coords, cell_list, game)

#def delete_cell:
   #pass

def add_cell(coords, cell_list, game):
    #initial window has two cols to acomodate addch()
    window = curses.newwin(1, 2, coords[0]+1, coords[1]+1) 
    window.bkgd(curses.color_pair(3)) 
    window.addch(curses.ACS_BULLET)

    window.resize(1,1) #correct window size to 1x1
    cell_list.append(window)

def display_help(window):
    curses.curs_set(0) #never  visible cursor
    size = window.getmaxyx()
    message = " ".join(["CONWAY'S GAME OF LIFE\n\n",
        "Move the cursor with **** WASD or KJHL"])

    help_pane = curses.newwin(6, 40, size[0]//2-3, size[1]//2-20) 
    help_pane.bkgd(curses.color_pair(2)) 

    help_pane.addstr(1,0,message)
    help_pane.addch(3,22,curses.ACS_UARROW)
    help_pane.addch(3,23,curses.ACS_DARROW)
    help_pane.addch(3,24,curses.ACS_LARROW)
    help_pane.addch(3,25,curses.ACS_RARROW)

    help_pane.getch()
    help_pane.erase

curses.wrapper(main) 
