from tarfile import RECORDSIZE
import numpy as np  #使用numpy库里的随机函数
#from .history import *
BLACK = 1  #棋盘格子属性 黑棋 白棋 无棋
WHITE = 2
EMPTY = 0

width = 15   #棋子宽度与高度
height = 15

directions = [      #表示格子的四个方向
    (0, 1),  # 0°
    (1, 1),  # 45°
    (1, 0),  # 90°
    (1,-1)   # 135°
]

def CreateGame(h, w):
    return np.zeros((h, w)).astype(np.uint8)  #使用库函数 生产一个15*15的矩阵 然后将其数据类型转化成无符号8位（最小的类型）

def CurStep(board): #非空格子数量
    res = 0
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            res += 1 if board[i,j] != 0 else 0
    return res
def Serialize(board):  #把棋盘转化成一个数字  用于哈希
    res = ''
    for i in range(board.shape[0]):
        tmp = 0
        for j in range(board.shape[1]):
            tmp = tmp * 3 + board[i,j]
        res += str(tmp)
    return res
def PositionInBoard(board, x, y):    #判断落子是否在棋盘内
    h, w = board.shape  
    return (0<=x) and (x<h) and (0<=y) and (y<w)

# stepFunc: 一个函数，调用获得落子地点
# 0 表示游戏还未结束
# 1 玩家1获胜
# 2 玩家2获胜
def Step(board, player, stepFunc):    #棋来！
    x, y = stepFunc(board, player)

    if(CurStep(board)==225): #和棋则白棋赢
        return 2,x,y
    # 判断是否合法
    if ((not PositionInBoard(board, x, y)) or board[x,y]!=EMPTY): #如果落子不合法 直接判对手赢
        printf("落子不合法")
        return 3 - player, x, y
    board[x, y] = player

    # 判断是否有玩家获胜
    for d in directions: 
        cnt = 1
        cx, cy = x, y
        while True:    #查询四个方向是否有五子连成
            cx += d[0]
            cy += d[1]
            if(PositionInBoard(board, cx, cy) and board[cx, cy] == player):
                cnt += 1
            else:
                break
        cx, cy = x, y  #返回起点
        while True:  #查询另外四个方向
            cx -= d[0]
            cy -= d[1]
            if(PositionInBoard(board, cx, cy) and board[cx, cy] == player):
                cnt += 1
            else:
                break
        
        if (cnt >= 5):  #判断赢家
            return player, x, y
    
    return 0, x, y     #如果没有赢家 继续

def Print(board):
    print('   ', end='')
    for j in range(board.shape[1]):
        print("%02d" % j, end=' ')
    print('')    #换行
    for i in range(board.shape[0]):
        print("%02d" % i, end='')
        for j in board[i]:
            if (j == EMPTY):
                print(' .', end=' ')
            elif (j == BLACK):
                print(' X', end=' ')
            else:
                print(' O', end=' ')
        print('') #换行

def Play(board, stepFuncs, display = True):
    Print(board)
    currentPlayer = 1   #当前为黑子
    history = [] 
    print("Game begins")
    while (True):
        print("Current Player {}".format(currentPlayer))   # print(f"Current Player {currentPlayer}") 也可以这样写
        res = Step(board, currentPlayer, stepFuncs[currentPlayer])[0]  #下棋 并获取结果
        if display:
            Print(board)
            history.append(Serialize(board))
        if (res != 0):
            print("Player {} wins".format(res))   #print(f"Player {res} wins")  
            break
        else:
            currentPlayer = 3 - currentPlayer  #切换对手
    for i in history:
        record[i][0]+=1
        record[i][res]+=1
    return res

def Player(board, player): 
    print("Player input as (x,y):")
    s = input()
    s = s.split(',') #以逗号为界分割
    return int(s[0]), int(s[1])
