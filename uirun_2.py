from doctest import BLANKLINE_MARKER
from re import X
from tkinter import Y
from .ui import *
from .rules import *
from .ai import *
def ui_Play(board, stepFuncs, display = True):
    currentPlayer = 1   #当前为黑子
    flag=True
    time=0
    F=True
    history = [] 
    pygame.init()
#获取对显示系统的访问，并创建一个窗口screen
#窗口大小位670x670
    screen=pygame.display.set_mode((670,670))
    screen_color=[238,153,73] #设置画布颜色，[238,154,73]对应为白色
    line_color=[0,0,0] #设置线条颜色，[0,0,0]对应黑色
    while True:
        for event in pygame.event.get(): #获取事件，如果鼠标点击右上角关闭按钮，关闭
            if event.type in (QUIT,KEYDOWN):
                sys.exit
        screen.fill(screen_color)#清屏
        for i in range(27,670,44):
            if i==27 or i==670-27:
                pygame.draw.line(screen,line_color,[i,27],[i,670-27],4)
            else:
                pygame.draw.line(screen,line_color,[i,27],[i,670-27],2)
        #再画横线
            if i==27 or i==670-27:
                pygame.draw.line(screen,line_color,[27,i],[670-27,i],4)
            else:
                pygame.draw.line(screen,line_color,[27,i],[670-27,i],2)
        pygame.draw.circle(screen,line_color,[27+44*7,27+44*7],8,0)
        pygame.draw.circle(screen,line_color,[27+44*3,27+44*3],8,0)
        pygame.draw.circle(screen,line_color,[27+44*3,27+44*11],8,0)
        pygame.draw.circle(screen,line_color,[27+44*11,27+44*3],8,0)
        pygame.draw.circle(screen,line_color,[27+44*11,27+44*11],8,0)
        if(flag):
            flag=False
            res = Step(board, currentPlayer, AIPlayer)  #下棋 并获取结果
            print("ai")
            x=res[1]
            y=res[2]
            Print(board)
            ui_step((x*44)+27,(y*44)+27,over_pos)
            history.append(Serialize(board))
        if (res[0]!= 0):
            print("Player {} wins".format(res[0]))   #print(f"Player {res} wins")  
        


        for val in over_pos:#显示所有落下的棋子
            pygame.draw.circle(screen, val[1],val[0], 20,0)
        cnt=check_win(over_pos)
        if cnt[0]!=0:
            for pos in cnt[1]:
                pygame.draw.rect(screen,[238,48,167],[pos[0]*44+27-22,pos[1]*44+27-22,44,44],2,1)
                #flag=False
                
            pygame.display.update()#刷新显示
            s=input() #游戏结束，停止下面的操作
         #获取鼠标坐标信息
        x,y = pygame.mouse.get_pos()

        x,y=find_pos(x,y)
        if check_over_pos(x,y,over_pos):#判断是否可以落子，再显示
            pygame.draw.rect(screen,[0 ,229 ,238 ],[x-22,y-22,44,44],2,1)

        keys_pressed = pygame.mouse.get_pressed()#获取鼠标按键信息
        #鼠标左键表示落子,tim用来延时的，因为每次循环时间间隔很断，容易导致明明只按了一次左键，却被多次获取，认为我按了多次
        if keys_pressed[0] and time==0:
            F=True
            ui_step(x,y,over_pos)
            x=int((x-27)/44)
            y=int((y-27)/44)
            print(x,y)
            board[x,y]=WHITE
            flag=True
        for val in over_pos:#显示所有落下的棋子
            pygame.draw.circle(screen, val[1],val[0], 20,0)
         #鼠标左键延时作用
        if F:
            time+=1
        if time%10==0:#延时10ms
            F=False
            time=0

        
        pygame.display.update()
    

    

    for i in history:
        if(i not in record):
            record[i]=[1,0,0]
            record[i][res]=1            
        else:
            record[i][0]+=1
            record[i][res]+=1
    
    return res


    



def ui_run():
    Load(0)
    board = CreateGame(height, width)
    ui_Play(board, [None, AIPlayer, AIPlayer], display=True)



if __name__ == '__main__':
    ui_run()