from .rules import *
from .ai import *

def TrainIter():
    board = CreateGame(height, width)
    Play(board, [None, AIPlayer, AIPlayer], display=True)


def Run():
    print("Loading previous results...")
    Load(0)
    print("Begin training.")
    cnt = 0
    while True:
        print("Iter", cnt)
        TrainIter()
        Dump(cnt % 4)
        cnt += 1

if __name__ == '__main__':
    Run()