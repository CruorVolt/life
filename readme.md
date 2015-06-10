#LIFE
Conway's game of life displayed in the terminal via curses.

##Basics
'python life' to start a blank game for editing,
'python life <filename>' to load a file with a pre-defined game state.

##File Format
Game states are in JSON format and contain a list of live cells in that state:

'''
{
  "cells": [
    {"y": 2, "x": 2}, 
    {"y": 3, "x": 3}, 
    {"y": 4, "x": 3}, 
    {"y": 4, "x": 2}, 
    {"y": 4, "x": 1}
  ]
}
'''

Cell locations will be shifted on load to be centered relative 
to the current window size. Some sample patterns are in 'patterns/'

##Controls
'''
Move cursor . . . . Arrow keys, WASD or KJHL

Paint/delete cell . . . . . . SPACE or ENTER

Next generation . . . . . . . . . . . . .  G

Run . . . . . . . . . . . . . . . . . . .  R

Change tick speed  . . . . . . . . . . . +/-

Output to file . . . . . . . . . . . . . . F

Display help info . . . . . . . . . . . .  I
'''
