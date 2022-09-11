from .rules import *
from .ai import *

board = CreateGame(height, width)
Play(board, [None, Player, AIPlayer])
