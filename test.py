import unittest
from life import *

class TestLife(unittest.TestCase):

    def setUp(self):
        #block still life
        self.game = Life( (10,10) )
        self.game.add_cell((1,1))
        self.game.add_cell((1,2))
        self.game.add_cell((2,1))
        self.game.add_cell((2,2))

    def tearDown(self):
        self.game = None

    def simple_tick_test(self):
        self.game.tick()
        block_game = Life( (10,10) )
        block_game.add_cell((1,1))
        block_game.add_cell((1,2))
        block_game.add_cell((2,1))
        block_game.add_cell((2,2))
        self.assertEqual(set(self.game.get_state()),set(block_game.get_state()), 
            'block game did not tick properly') 

    def glider_tick_test

if __name__ == '__main__':
    unittest.main()

#assertEqual
#assertTrue
#assertFalse
#assertRaises(TypeError)
