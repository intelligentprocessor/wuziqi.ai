from .rules import *
from .ai import *

board = CreateGame(height, width) #建一个棋盘
Play(board, [None, Player, AIPlayer])  #设定为黑棋为人 白棋为ai
