from .rules import *
import random
import json
import math

attempts = 25
totAttempts = 4000
curAttempts = 0
record = {}

def Load(fileId):
    fileName = "./wuziqi/record/file%d.json" % fileId
    with open(fileName, 'r') as f:
        record=json.load(f)

def Dump(fileId):
    fileName = "./wuziqi/record/file%d.json" % fileId
    with open(fileName, 'w') as f:
        json.dump(record,f)

def CurStep(board):
    res = 0
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            res += 1 if board[i,j] != 0 else 0
    return res

def Serialize(board):
    res = ''
    for i in range(board.shape[0]):
        tmp = 0
        for j in range(board.shape[1]):
            tmp = tmp * 3 + board[i,j]
        res += str(tmp)
    return res

def GetLegalPositions(board):
    res = []
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i,j] == EMPTY:
                res.append((i,j))
    return res

def RandomStep(legal, value):
    item = np.random.choice(range(value.shape[0]), 1, True, value)[0]
    return legal[item]

def ValueFunc(board, player, pos):
    x, y = pos
    value = 0

    if pos[0] == 0 or pos[0] == board.shape[0] or pos[1] == 0 or pos[1] == board.shape[1]:
        value -= 1

    # 先找自己能挡多少
    for d in directions:
        cnt = 0
        cx, cy = x, y
        while True:
            cx += d[0]
            cy += d[1]
            if(PositionInBoard(board, cx, cy) and board[cx, cy] == 3-player):
                cnt += 1
            else:
                break
        cx, cy = x, y
        while True:
            cx -= d[0]
            cy -= d[1]
            if(PositionInBoard(board, cx, cy) and board[cx, cy] == 3-player):
                cnt += 1
            else:
                break
        
        if (cnt >= 3):
            value += 20
        elif (cnt >= 2):
            value += 8
        elif (cnt >= 1):
            value += 2

    # 再找自己能连多少
    numberOf3 = 0
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
            value += 100
        if (cnt >= 4):
            value += 20
        elif (cnt >= 3):
            value += 8
        elif (cnt >= 2):
            value += 4
        elif (cnt >= 1):
            value += 2

        if (cnt >= 3):
            numberOf3 += 1
    if numberOf3 >= 2:
        value += 20
    
    return value

def MCTS(board, player, depth):
    global curAttempts
    legal = GetLegalPositions(board)

    value = []
    for i in legal:
        v = ValueFunc(board,player,i)
        value.append(v)
    value = np.array(value, dtype=np.float)
    value = np.exp(value) / np.sum(np.exp(value))
    if (value.shape[0] == 0):
        return 0, 1

    id = Serialize(board)
    if (id not in record):
        record[id] = [0, 0, 0]

    localTot = 0
    localWin = 0

    for i in range(math.ceil(attempts / (depth+1))):
        curAttempts += 1
        if curAttempts > totAttempts:
            break

        win, x, y = Step(board, player, (lambda board, player: RandomStep(legal, value)) )

        if (win == 0):
            childWin, childTot = MCTS(board, 3-player, depth+1)

            record[id][player] += childTot - childWin
            record[id][3-player] += childWin
            record[id][0] += childTot
            
            localWin += childTot - childWin
            localTot += childTot
        else:
            record[id][win] += 1
            record[id][0] += 1
            
            localWin += 1 if win == player else 0
            localTot += 1
            
        board[x, y] = EMPTY

    return (localWin, localTot)


def AIPlayer(board, player):
    global curAttempts
    curAttempts = 0

    print("AI thinking...")

    if (CurStep(board) == 0):
        return (board.shape[0])//2, (board.shape[1])//2

    MCTS(board, player, 0)

    legal = GetLegalPositions(board)
    maxi = -1
    maxpos = (0, 0)
    for i in legal:
        board[i[0], i[1]] = player
        id = Serialize(board)
        if id not in record:
            board[i[0], i[1]] = EMPTY
            continue
        item = record[id]
        if (item[player] / item[0] >= maxi):
            maxi = item[player] / item[0]
            maxpos = i
        board[i[0], i[1]] = EMPTY
    
    print("Max pos =", maxpos, ", prob. of win:", maxi)
    return maxpos