import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from game import *

import copy
import itertools

def empty_game():
	game = Game(board=None,c_score=0)
	game.x = copy.deepcopy(Game.x) #using deepcopy to not reflect any other child of this object
	game.copy_board = game.x[:]
	game.c_score = Game.c_score
	return game

import unittest



class TestEmptyBoard(unittest.TestCase):
	def setUp(self):
		self.game = empty_game()



	def test_board_size(self):
		self.assertEqual(len(self.game.x), 4)
		self.assertEqual(len(self.game.x[0]), 4)


	def test_board_rotate(self):
		self.game.x[0][0] = 8
		self.game.rotate(2)
		self.assertEqual(self.game.x[3][3],8)

	def test_move(self):
		self.game.x[0][0] = 8
		self.game.process_move("d")
		self.assertEqual(self.game.x[0][3],8)
		self.game.process_move("s")
		self.assertEqual(self.game.x[3][3],8)
		self.game.process_move("a")
		self.assertEqual(self.game.x[3][0],8)
		self.game.process_move("w")
		self.assertEqual(self.game.x[0][0],8)

	def test_sum_up(self):
		self.game.x[2][0] = 4
		self.game.x[3][0] = 4
		self.game.sum_up()
		self.assertEqual(self.game.x[2][0],8)
		self.assertEqual(self.game.x[3][0],0)

	def test_count_score(self):
		self.game.x[2][0] = 4
		self.game.x[3][0] = 4
		#print(self.game.x)
		self.game.sum_up()
		#print(self.game.x)
		self.assertEqual(self.game.c_score,8)

	def test_gravity(self):
		# move elements to the bottom on the Y-axis
		
		self.game.x[0][2] = 8
		self.game.x[1][3] = 32
		self.game.x[3][2] = 8

		# printing just to see what happens in CLI
		# and making the display behave like 'gravity' in CLI
		"""
		print()		
		for p in self.game.x[::-1]: 
			print(p)
		print()
		"""
		self.game.gravity()
		"""
		for p in self.game.x[::-1]:
			print(p)
		print()
		"""

		self.assertEqual(self.game.x[0][3],32)
		self.assertEqual(self.game.x[1][2],8)

		
		##### TESTING WITH RANDOMLY ADDED NUMBER(S) #####
		

	def test_new_board(self):
		self.game.new_board()
		matrix_list = list(itertools.chain.from_iterable(self.game.x)) #making a list from the matrix to use assertion
		self.assertTrue(2 in matrix_list or 4 in matrix_list)

	def test_randomboard_gravity(self):
		self.game.new_board()
		self.game.gravity()
		#print(self.game.x[0])
		self.assertTrue(2 in self.game.x[0] or 4 in self.game.x[0])


		##### TESTING "COPY" METHODS #####


	def test_gravity_copy(self):
		# move elements to the bottom on the Y-axis
		
		self.game.copy_board[0][2] = 8
		self.game.copy_board[1][3] = 32
		self.game.copy_board[3][2] = 8

		# printing just to see what happens in CLI
		# and making the display behave like 'gravity' in CLI
		"""
		print()		
		for p in self.game.x[::-1]: 
			print(p)
		print()
		"""
		self.game.gravity_copy()
		"""
		for p in self.game.x[::-1]:
			print(p)
		print()
		"""

		self.assertEqual(self.game.copy_board[0][3],32)
		self.assertEqual(self.game.copy_board[1][2],8)	

	def test_sum_up_copy(self):
		self.game.copy_board[2][0] = 4
		self.game.copy_board[3][0] = 4
		self.game.sum_up_copy()
		self.assertEqual(self.game.copy_board[2][0],8)
		self.assertEqual(self.game.copy_board[3][0],0)

	def test_rotate_copy(self):
		self.game.copy_board[0][0] = 8
		self.game.rotate(2)
		self.assertEqual(self.game.copy_board[3][3],8)

	def test_move_copy(self):
		self.game.copy_board[0][0] = 8
		self.game.process_move_copy("d")
		self.assertEqual(self.game.copy_board[0][3],8)
		self.game.process_move_copy("s")
		self.assertEqual(self.game.copy_board[3][3],8)
		self.game.process_move_copy("a")
		self.assertEqual(self.game.copy_board[3][0],8)
		self.game.process_move_copy("w")
		self.assertEqual(self.game.copy_board[0][0],8)

if __name__ == '__main__':
	unittest.main()