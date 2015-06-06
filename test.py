import unittest
from life import *

class TestLife(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        self.game = None

    def test_static_block(self):
        block_game = Life( (10,10) )
        block_game.add_cell((1,1))
        block_game.add_cell((1,2))
        block_game.add_cell((2,1))
        block_game.add_cell((2,2))

        initial_state = block_game.get_state()
        block_game.tick()
        advanced_state = block_game.get_state()

        self.assertEqual(set(initial_state),set(advanced_state), 
            'block game did not tick properly') 

    def test_glider(self):
        
        #initial glider state
        glider_game = Life( (6,6) )        
        glider_game.add_cell((1,3))
        glider_game.add_cell((2,4))
        glider_game.add_cell((3,4))
        glider_game.add_cell((3,3))
        glider_game.add_cell((3,2))

        glider_game.tick()
        state1 = glider_game.get_state()

        #advanced glider state
        glider_game_2 = Life( (6,6) )        
        glider_game_2.add_cell((2,2))
        glider_game_2.add_cell((2,4))
        glider_game_2.add_cell((3,3))
        glider_game_2.add_cell((3,4))
        glider_game_2.add_cell((4,3))
        state2 = glider_game_2.get_state()

        self.assertEqual(set(state1),set(state2), 
            'glider game did not tick properly') 

    def test_toggle_cell(self):
        test_game = Life( (10,10) )
        test_game.add_cell((5,5))
        test_game.add_cell((4,4))
        test_game.add_cell((3,3))
        test_game.add_cell((2,2))
        test_game.toggle_cell((1,1))
        test_game.toggle_cell((2,2))
        test_game.toggle_cell((3,3))

        game_set = set(test_game.get_state())
        ground_set = set([(1,1), (4,4), (5,5)])

        self.assertEqual(game_set, ground_set, "toggle_cell add/delete error")

if __name__ == '__main__':
    unittest.main()
