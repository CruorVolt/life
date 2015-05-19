import curses.wrapper
import life

def main(screen): 

    curses.start_color() 

    curses.echo

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_GREEN)
    screen.bkgd(curses.color_pair(2)) 
    screen.refresh() 

    y,x = screen.getmaxyx()
    win = curses.newwin(y-1, x-2, 1, 1) 
    win.bkgd(curses.color_pair(0)) 
    win.addstr(2, 2, "text") 
    win.refresh() 

    borderwin = curses.newwin(1, x, y-1, 0)
    borderwin.bkgd(curses.color_pair(1))
    borderwin.addstr(0,0,"BORDER")
    borderwin.refresh() 

    blockwin = curses.newwin(1, 1, 10, 10)
    blockwin.bkgd(curses.color_pair(3))
    blockwin.refresh() 

    curses.setsyx(y//2,x//2)

    while 1:
        c = screen.getch()
        cursor_y, cursor_x = screen.getyx()
        if c == ord('q') or c == 27:
            exit()
        elif c == curses.KEY_LEFT:
            win.move(cursor_y, cursor_x - 1)
        elif c == curses.KEY_RIGHT:
            win.move(cursor_y, cursor_x + 1)
        elif c == curses.KEY_UP:
            win.move(cursor_y - 1, cursor_x)
        elif c == curses.KEY_DOWN:
            win.move(cursor_y +1, cursor_x)
        win.refresh()

def move_cursor(window, new_x, new_y):
    '''Moves the cursor to the new location, respecting window edges.

    window is the curses window object with the cursor to be moved. 
    new_x and new_y are the desired x and y coordinates of the cursor.
    move_cursor will either modify the window to hav the cursor set at
    the new location or do nothing if the desired coordinates are outside
    the window's borders.
    '''

curses.wrapper(main) 
