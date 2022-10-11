from .rules import *
from .ai import *

board = CreateGame(height, width) #建一个棋盘
Play(board, [None, Player, AIPlayer])  #设定为黑棋为ai 白棋为人
