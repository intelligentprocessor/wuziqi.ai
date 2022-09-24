from .rules import *
import random
import json
import math

attempts = 25   #分支数
totAttempts = 4000   #计算下一步的最大时间
curAttempts = 0  #当前已经算了多少时间
record = {}   #  训练数据数组

def Load(fileId):  #读文件
    fileName = "./wuziqi/record/file%d.json" % fileId   #分散为10个文件
    with open(fileName, 'r') as f:
        record=json.load(f)

def Dump(fileId):  #写文件
    fileName = "./wuziqi/record/file%d.json" % fileId   #分散为10个文件
    with open(fileName, 'w') as f:
        json.dump(record,f)

def CurStep(board):  #返回空格子数量
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

def GetLegalPositions(board):   #返回可下的棋盘格子列表
    res = []
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i,j] == EMPTY:
                res.append((i,j))
    return res

def RandomStep(legal, value):   #按照value的概率从value下标随机取一个数 返回要在legal落子的点
    item = np.random.choice(range(value.shape[0]), 1, True, value)[0]
    return legal[item]

def ValueFunc(board, player, pos): #获取落点基于规则的启发value
    x, y = pos
    value = 0

    if pos[0] == 0 or pos[0] == board.shape[0] or pos[1] == 0 or pos[1] == board.shape[1]:  #边缘下棋value--
        value -= 1

    # 先找自己能挡多少
    for d in directions:
        cnt = 0
        cx, cy = x, y
        while True:
            cx += d[0]
            cy += d[1]
            if(PositionInBoard(board, cx, cy) and board[cx, cy] == 3-player): #没挡到就break
                cnt += 1
            else:
                break
        cx, cy = x, y
        while True:
            cx -= d[0]
            cy -= d[1]
            if(PositionInBoard(board, cx, cy) and board[cx, cy] == 3-player):#没挡到就break
                cnt += 1
            else:
                break
        if(cnt>=4):
            value += 100
        elif (cnt >= 3):
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
            if(PositionInBoard(board, cx, cy) and board[cx, cy] == player):#没连到就break
                cnt += 1
            else:
                break
        cx, cy = x, y
        while True:
            cx -= d[0]
            cy -= d[1]
            if(PositionInBoard(board, cx, cy) and board[cx, cy] == player):#没连到就break
                cnt += 1
            else:
                break
        
        if (cnt >= 5):
            value += 100
        elif (cnt >= 4):
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
    value = np.array(value, dtype=np.float)  #将value转化成float类型
    value = np.exp(value) / np.sum(np.exp(value))  #exp是对整个向量进行运算 然后/所有的结果之和
    if (value.shape[0] == 0):
        return 0, 1

    id = Serialize(board)  #获取哈希后的棋盘
    if (id not in record):
        record[id] = [0, 0, 0]

    localTot = 0 
    localWin = 0 

    for i in range(math.ceil((attempts / (depth+1))+1)):  #向上舍入  搜索宽度越往下越窄
        curAttempts += 1
        if curAttempts > totAttempts:  #搜索时间过大 退出
            break

        win, x, y = Step(board, player, (lambda board, player: RandomStep(legal, value)) )

        if (win == 0):
            childWin, childTot = MCTS(board, 3-player, depth)  #获取对手mcts返回的胜利次数和总次数

            record[id][player] += childTot - childWin  #胜利次数
            record[id][3-player] += childWin   #失败次数
            record[id][0] += childTot    #总次数
            localWin += childTot - childWin  #字节点总共胜利次数
            localTot += childTot    #子节点总共次数
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

    legal =GetLegalPositions(board)
    father_id=Serialize(board)
    father_item=record[father_id]
    maxi = -1
    mini=-2
    maxpos = (0, 0)
    for i in legal:
        board[i[0], i[1]] = player
        id = Serialize(board)
        item = record[id]
        if (id not in record):
            value=ValueFunc(board, player, i)
            if((value>mini) and (maxi==-1)):
                mini=value
                maxpos=i
        elif ((item[player] / item[0]+math.sqrt(2*math.log(father_item[0])/item[0])) >= maxi):
            maxi = item[player] / item[0]
            maxpos = i
        board[i[0], i[1]] = EMPTY
   
    print("Max pos =", maxpos, ", prob. of win:", maxi)
    return maxpos