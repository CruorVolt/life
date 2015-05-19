import curses.wrapper
import life

def main(screen): 

    curses.start_color() 

    curses.curs_set(2) #always visible cursor

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_GREEN)
    screen.bkgd(curses.color_pair(2)) 
    screen.refresh() 

    y,x = screen.getmaxyx()
    win = curses.newwin(y-1, x-2, 1, 1) 
    win.bkgd(curses.color_pair(0)) 
    win.refresh() 

    borderwin = curses.newwin(1, x, y-1, 0)
    borderwin.bkgd(curses.color_pair(1))
    borderwin.addstr(0,0,"BORDER")
    borderwin.refresh() 

    #blockwin = curses.newwin(1, 1, 10, 10)
    #blockwin.bkgd(curses.color_pair(3))
    #blockwin.refresh() 

    curses.setsyx(y//2,x//2)

    while 1:
        c = screen.getch()
        cursor_y, cursor_x = win.getyx()
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

        borderwin.addstr(0,0, "Cursor at Y={y}, X={x}".format(y=cursor_y, x=cursor_x))
        borderwin.refresh()
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
    if new_y >= 0 and new_x >= 0 and new_y < max_y-1 and new_x < max_x:
        window.move(new_y, new_x)

curses.wrapper(main) 
