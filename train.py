from .rules import *
from .ai import *

def TrainIter():
    board = CreateGame(height, width)
    Play(board, [None, AIPlayer, AIPlayer], display=True)

Load(0)
cnt = 0
while True:
    print("Iter", cnt)
    TrainIter()
    Dump(cnt % 4)