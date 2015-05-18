import curses.wrapper

def main(screen): 
    curses.start_color() 

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    screen.bkgd(curses.color_pair(2)) 
    screen.refresh() 

    y,x = screen.getmaxyx()
    win = curses.newwin(y-1, x-2, 1, 1) 
    win.bkgd(curses.color_pair(0)) 
    win.addstr(2, 2, "GREETINGS") 
    win.refresh() 

    borderwin = curses.newwin(1, x, y-1, 0)
    borderwin.bkgd(curses.color_pair(1))
    borderwin.addstr(0,0,"BORDER")
    borderwin.refresh() 

    c = screen.getch() 

try: 
    curses.wrapper(main) 
except KeyboardInterrupt: 
    print "EXITING" 
    exit() 
