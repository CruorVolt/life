import curses
import time
import sys
from curses import wrapper
from decimal import Decimal

import reader
from life import *

MIN_TICK = Decimal('0.01')
MAX_TICK = Decimal('5.00')

class LifeDisplay:

    def __init__(self):
        self.cell_list = {} #curses window objects returned by newwin()
        self.game = None
        self.current_cursor = None
        self.borderwin = None
        self.wait_time = Decimal('0.01') #millisecond precision for addition
        try:
            wrapper(self.init_curses)

        #Handle all errors here so wrapper can exit properly
        except curses.error:
            print("ERROR: current terminal not large enough for proper display")
        except CellOutOfBounds:
            print("ERROR: specified game state does not fit in this window")
        except IOError as io:
            if len(io.args) < 1:
                print("ERROR: File read problem")
            else:
                print("ERROR: File '{file}' not found".format(file=io.args[0]))


    def init_curses(self, screen):
        '''
        Everything the board needs to display properly.
        expects to get screen from being called by curses.wrapper()
        '''

        self.screen = screen
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

        pattern = reader.parse_args()
        self.game = Life((y-2,x-2), pattern)

        for col in range(1,y-2):
            for row in range(1, x-2):
                new_win = curses.newwin(1,1,col,row)
                new_win.bkgd(curses.color_pair(2))
                new_win.refresh() #or they won't fill the background right
                self.cell_list[(col,row)] = new_win

        self.move_cursor(screen, (y//2, x//2))

        self.borderwin = curses.newwin(1, x, y-1, 0)
        self.borderwin.bkgd(curses.color_pair(1))
        self.borderwin.addstr(0, x-30, "G-Step  R-Run  I-Info  Q-Quit")
        self.paint_cells()
        self.refresh_border()

        self.get_input();

    def get_input(self):
        while 1: #loop until getch sends exit()
            screen = self.screen
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
            elif c == ord('f'): #write pattern to file
                self.save_dialog(screen)
            elif c == ord('e'): #clear board
                self.clear()

            self.refresh_border()

    def refresh_border(self):
        try:
            #leave extra space for more digits
            self.borderwin.addstr(0,0,"Cursor at {y},{x}      ".format(
                y = self.current_cursor[0], x = self.current_cursor[1]))
            self.borderwin.addstr(0,24, "Live Cells: {cells}   ".format(
                cells=self.game.cell_count()))
            self.borderwin.addstr(0,43, "Tick Delay: {:1.0f} ms   ".format(
                self.wait_time * 100))
            self.borderwin.refresh()
        except curses.error: raise

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
    
        max_y,max_x = window.getmaxyx()
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
        header_message = "        CONWAY'S  GAME  OF  LIFE --- CONTROLS"
        message = "".join([
            " **** WASD or KJHL . . . . . . . . . . Move cursor\n\n",
            " SPACE/ENTER . . . . . . . . . . Paint/remove cell\n\n",
            " G . . . . . . . . . . . . Step through generation\n\n",
            " R . . . . . . . . . . . . . . . . . . . . . . Run\n\n",
            " +-  . . . . . . . . . . . . . . Change tick speed\n\n",
            " Q . . . . . . . . . . . . . . . . . . . . .  Quit\n\n\n",
            "             (press any key to close)"
        ])

        header_pane = curses.newwin(3,52, size[0]//2-6, size[1]//2-26)
        header_pane.bkgd(curses.color_pair(5)) 
        help_pane = curses.newwin(15, 52, size[0]//2-6+3, size[1]//2-26) 
        help_pane.bkgd(curses.color_pair(1)) 
    
        header_pane.addstr(1,0,header_message)
        help_pane.addstr(1,0,message)
        help_pane.addch(1,1,curses.ACS_UARROW)
        help_pane.addch(1,2,curses.ACS_DARROW)
        help_pane.addch(1,3,curses.ACS_LARROW)
        help_pane.addch(1,4,curses.ACS_RARROW)
        header_pane.refresh()
    
        help_pane.getch()

        help_pane.clear()
        help_pane.bkgd(curses.color_pair(6)) 
        help_pane.refresh()

        header_pane.clear()
        header_pane.bkgd(curses.color_pair(6)) 
        header_pane.refresh()
        self.paint_cells()

    def save_dialog(self, window):
        size = window.getmaxyx()
        message = "          SAVE PATTERN TO FILE\n\n Enter file name > "

        dialog = curses.newwin(5, 50, size[0]//2-3, size[1]//2-25) 
        dialog.bkgd(curses.color_pair(1)) 
    
        dialog.addstr(1,1,message)
    
        curses.echo()
        filename = dialog.getstr() #byte array for some reason
        dialog.clear()
        if reader.write_pattern_file(filename, self.game):
            dialog.bkgd(curses.color_pair(6))
            alert = 'FILE {} WRITTEN'.format(str(filename)[1:20]) #strip 'b' indicator
        else:
            dialog.bkgd(curses.color_pair(4))
            alert = "NO FILE WRITTEN"
        dialog.addstr(2, 24 - len(alert)//2, alert)
        dialog.refresh()
        time.sleep(1)

        curses.noecho()
        self.paint_cells()

    def increment_wait(self, milliseconds_change):
        self.wait_time += milliseconds_change
        if self.wait_time < MIN_TICK:
            self.wait_time = MIN_TICK
        elif self.wait_time > MAX_TICK:
            self.wait_time = MAX_TICK
