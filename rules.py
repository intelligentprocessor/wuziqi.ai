import numpy as np

BLACK = 1
WHITE = 2
EMPTY = 0

width = 15
height = 15

directions = [
    (0, 1),  # 0°
    (1,1),  # 45°
    (1,0),  # 90°
    (1,-1)   # 135°
]

def CreateGame(h, w):
    return np.zeros((h, w)).astype(np.uint8)

def PositionInBoard(board, x, y):
    h, w = board.shape
    return (0<=x) and (x<h) and (0<=y) and (y<w)

# stepFunc: 一个函数，调用获得落子地点
# 0 表示游戏还未结束
# 1 玩家1获胜
# 2 玩家2获胜
def Step(board, player, stepFunc):
    x, y = stepFunc(board, player)

    # 判断是否合法
    if ((not PositionInBoard(board, x, y)) or board[x,y]!=EMPTY):
        return 3 - player, x, y
    board[x, y] = player

    # 判断是否有玩家获胜
    for d in directions:
        cnt = 1
        cx, cy = x, y
        while True:
            cx += d[0]
            cy += d[1]
            if(PositionInBoard(board, cx, cy) and board[cx, cy] == player):
                cnt += 1
            else:
                break
        cx, cy = x, y
        while True:
            cx -= d[0]
            cy -= d[1]
            if(PositionInBoard(board, cx, cy) and board[cx, cy] == player):
                cnt += 1
            else:
                break
        
        if (cnt >= 5):
            return player, x, y
    
    return 0, x, y

def Print(board):
    print('   ', end='')
    for j in range(board.shape[1]):
        print("%02d" % j, end=' ')
    print('')
    for i in range(board.shape[0]):
        print("%02d" % i, end='')
        for j in board[i]:
            if (j == EMPTY):
                print(' .', end=' ')
            elif (j == BLACK):
                print(' X', end=' ')
            else:
                print(' O', end=' ')
        print('')

def Play(board, stepFuncs, display = True):
    Print(board)
    currentPlayer = 1
    print("Game begins")
    while (True):
        print("Current Player {}".format(currentPlayer))
        res = Step(board, currentPlayer, stepFuncs[currentPlayer])[0]
        if display:
            Print(board)
        if (res != 0):
            print("Player {} wins".format(res))
            break
        else:
            currentPlayer = 3 - currentPlayer
    return res

def Player(board, player):
    print("Player input as (x,y):")
    s = input()
    s = s.split(',')
    return int(s[0]), int(s[1])
