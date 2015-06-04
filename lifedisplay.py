import curses
import time
from curses import wrapper
from decimal import Decimal

from life import Life

MIN_TICK = Decimal('0.01')
MAX_TICK = Decimal('5.00')

class LifeDisplay:

    def __init__(self):
        self.cell_list = {} #curses window objects returned by newwin()
        self.game = None
        self.current_cursor = None
        self.borderwin = None
        self.wait_time = Decimal('0.01') #millisecond precision for addition
        wrapper(self.init_curses)


    def init_curses(self, screen):
        curses.start_color() 
        #curses.raw()
        #curses.cbreak()
        curses.curs_set(0) #never visible cursor

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) #bottom frame
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK) #dead cell
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN) #new cell
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_RED) #cursor
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLUE) #survived cell
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN) #border

        screen.bkgd(curses.color_pair(6)) 
        screen.refresh() 

        y,x = screen.getmaxyx()

        for col in range(1,y-2):
            for row in range(1, x-2):
                new_win = curses.newwin(1,1,col,row)
                new_win.bkgd(curses.color_pair(2))
                new_win.refresh() #or they won't fill the background right
                self.cell_list[(col,row)] = new_win

        self.move_cursor(screen, (y//2, x//2))

        self.game = Life( (y-2,x-2) )

        self.borderwin = curses.newwin(1, x, y-1, 0)
        self.borderwin.bkgd(curses.color_pair(1))
        self.borderwin.addstr(0, x-23, "G-Step  R-Run  I-Info")
        self.refresh_border()

        while 1:
            c = screen.getch()
            cursor_y, cursor_x = self.current_cursor
            if c == ord('q') or c == 27: #exit curses
                exit()
            elif c in [curses.KEY_LEFT, ord('a'), ord('h')]: #cursor left
                 self.move_cursor(screen, (cursor_y, cursor_x - 1))
            elif c in [curses.KEY_RIGHT, ord('d'), ord('l')]: #cursor right
                 self.move_cursor(screen, (cursor_y, cursor_x + 1))
            elif c in [curses.KEY_UP, ord('w'), ord('k')]: #cursor up
                 self.move_cursor(screen, (cursor_y - 1, cursor_x))
            elif c in [curses.KEY_DOWN, ord('s'), ord('j')]: #cursor down
                 self.move_cursor(screen, (cursor_y + 1, cursor_x))
            elif c == 10 or c == 32: #paint cell
                self.draw_cell((cursor_y, cursor_x))
            elif c == ord('i'): #display info
                self.display_help(screen)
            elif c == ord('g'): #step
                self.step()
                curses.flushinp() #cancel buffer: no lag on holding down key
            elif c == ord('r'): #run
                self.run(screen)
            elif c == ord('-'): #tick delay up (+)
                self.increment_wait(Decimal('-0.01'))
            elif c == ord('='): #tick delay down (-)
                self.increment_wait(Decimal('0.01'))
            elif c == ord('e'): #clear board
                self.clear()

            self.refresh_border()

    def refresh_border(self):

        #leave extra space for more digits
        self.borderwin.addstr(0,0,"Cursor at {y},{x}      ".format(
            y = self.current_cursor[0], x = self.current_cursor[1]))
        self.borderwin.addstr(0,24, "Live Cells: {cells}   ".format(
            cells=self.game.cell_count()))
        self.borderwin.addstr(0,43, "Tick Delay: {:1.0f} ms   ".format(
            self.wait_time * 100))
        self.borderwin.refresh()

    def clear(self):
        pass

    def move_cursor(self, window, new_cell):
        '''Moves the cursor to the new location, respecting window edges.

        window is the curses window object with the cursor to be moved. 
        new_x and new_y are the desired x and y coordinates of the cursor.
        move_cursor will either modify the window to hav the cursor set at
        the new location or do nothing if the desired coordinates are outside
        the window's borders.
        '''
    
        max_y, max_x = window.getmaxyx()
        new_y, new_x = new_cell
        if new_y > 0 and new_x > 0 and new_y < max_y-2 and new_x < max_x-2:
            if self.current_cursor:
                if self.game.has_cell(self.current_cursor):
                    self.cell_list[self.current_cursor].bkgd(curses.color_pair(3)) #repaint live
                else:
                    self.cell_list[self.current_cursor].bkgd(curses.color_pair(2)) #repaint dead
                self.cell_list[self.current_cursor].refresh()
            self.cell_list[new_cell].bkgd(curses.color_pair(4)) #paint new cursor
            self.cell_list[new_cell].refresh()
            self.current_cursor = new_cell
    
    def draw_cell(self, coords):
        cell_exists = self.game.toggle_cell(coords)
        if cell_exists:
            self.delete_cell(coords)
        else:
    	    self.add_cell(coords)
    
    def delete_cell(self, coords):
        pass
    
    def add_cell(self, coords):
        window = curses.newwin(1, 2, coords[0]+1, coords[1]+1) 
        self.cell_list[coords].bkgd(curses.color_pair(3)) #live color
        self.cell_list[coords].refresh()
    
    def step(self):
        game_state = self.game.get_state()
    
        self.game.tick()
    
        new_state = self.game.get_state() #THIS COPY PROCEDURE DOES NOT WORK
    
        for coords in self.cell_list.keys():
            window = self.cell_list[coords]
            if self.game.has_cell(coords):
                if coords in game_state:
                    window.bkgd(curses.color_pair(5)) #this cell survived
                else:
                    window.bkgd(curses.color_pair(3)) #this cell is alive
            else:
                window.bkgd(curses.color_pair(2)) #this cell is dead
            window.refresh()
        self.refresh_border()

    def run(self, main_window):
        self.borderwin.bkgd(curses.color_pair(4)) #inactive background
        self.refresh_border()
        main_window.nodelay(1) #getch becomes non-blocking
        while 1:
            self.step()
            time.sleep(self.wait_time)
            c = main_window.getch()
            if c != -1: #wait for any press
                break
        main_window.nodelay(0) #reset getch behavior
        self.borderwin.bkgd(curses.color_pair(1)) #reset color
        self.refresh_border()
    
    def paint_cells(self):
        for coords in self.cell_list.keys():
            window = self.cell_list[coords]
            if self.current_cursor == coords:
                window.bkgd(curses.color_pair(4)) #redraw cursor location
            elif self.game.has_cell(coords):
                window.bkgd(curses.color_pair(3)) #this cell is alive
            else:
                window.bkgd(curses.color_pair(2)) #this cell is dead
            window.refresh()

    def display_help(self, window):
        size = window.getmaxyx()
        message = " ".join(["        CONWAY'S  GAME  OF  LIFE\n\n",
            "   Move the cursor with **** WASD or KJHL\n\n",
            "   Paint/delete cells with SPACE or ENTER\n\n",
            "Step through generations with G   Run with R\n\n",
            "            Change tick speed: +-\n\n",
            "           (press any key to close)"])

        header_message = "        CONWAY'S  GAME  OF  LIFE --- CONTROLS"
    
        message = "".join([
            "    **** WASD or KJHL --- Move cursor\n\n",
            "          SPACE/ENTER --- Paint \& delete cells\n\n",
            "                    G --- Step through generation\n\n",
            "                    R --- Run\n\n",
            "                   +- --- Change tick speed: n\n\n\n",
            "           (press any key to close)"
        ])

        #header_pane = curses.newwin(3,52, size[0]//2-6+10, size[1]//2-26)
        header_pane = curses.newwin(3,52, 1,1)
        header_pane.bkgd(curses.color_pair(1)) 
        help_pane = curses.newwin(13, 52, size[0]//2-6+3, size[1]//2-26) 
        help_pane.bkgd(curses.color_pair(6)) 
    
        header_pane.addstr(1,0,header_message)
        help_pane.addstr(1,0,message)
        help_pane.addch(3,4,curses.ACS_UARROW)
        help_pane.addch(3,5,curses.ACS_DARROW)
        help_pane.addch(3,6,curses.ACS_LARROW)
        help_pane.addch(3,7,curses.ACS_RARROW)
    
        help_pane.getch()
        help_pane.erase()
        self.paint_cells()

    def increment_wait(self, milliseconds_change):
        self.wait_time += milliseconds_change
        if self.wait_time < MIN_TICK:
            self.wait_time = MIN_TICK
        elif self.wait_time > MAX_TICK:
            self.wait_time = MAX_TICK
