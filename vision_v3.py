import pyscreeze as pg
import time
from PIL import Image
from stockfish import Stockfish
import cv2
import numpy as np
import utility


board_size = 792
block_size = 99

let_l = []
num_l = []


pieces_all = ['wp','wb','wk','wn','wq','wr','bp','bb','bk','bn','bq','br']

lett = {0:'a',99:'b',198:'c',297:'d',396:'e',495:'f',594:'g',693:'h'}
numm = {0:'8',99:'7',198:'6',297:'5',396:'4',495:'3',594:'2',693:'1'}

n_ = []
o_ = []
o = 0

opp = []
now = []

stockfish = Stockfish(path=r"Path to stockfish exe",
                      depth=22, parameters={"Threads": 4, "Minimum Thinking Time": 30, 'Hash':1024, "UCI_Chess960": "true"})

#this is the chess board
r0 = ['E','E','E','E','E','E','E','E']
r1 = ['E','E','E','E','E','E','E','E']
r2 = ['E','E','E','E','E','E','E','E']
r3 = ['E','E','E','E','E','E','E','E']
r4 = ['E','E','E','E','E','E','E','E']
r5 = ['E','E','E','E','E','E','E','E']
r6 = ['E','E','E','E','E','E','E','E']
r7 = ['E','E','E','E','E','E','E','E']

all_rows = [r0,r1,r2,r3,r4,r5,r6,r7]

row_place = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
row_ = {'1':r7,'2':r6,'3':r5,'4':r4,'5':r3,'6':r2,'7':r1,'8':r0}


def c2(img):

    blackcolor = [113, 105, 76]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img[np.all(img == blackcolor + [255], axis=2)] = [0,0,0,0]
   
    cv2.imwrite('outpgut.png',img)
    return img


def board_p():
    value = 0.70
    b = Image.open('photos/board.png')
    b.thumbnail((board_size, board_size))
    board_onscreen = pg.locateOnScreen(image=b, grayscale=True, confidence=0.70)
    return(board_onscreen)

def clean(img):
    blackcolor = [133, 133, 133]
    whitecolor = [235, 235, 235]
    img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    img[np.all(img == blackcolor + [255], axis=2)] = [0,0,0,0]
    img[np.all(img == whitecolor + [255], axis=2)] = [0,0,0,0]
    cv2.imwrite('output.png',img)
    return img

def fill():
    x = 0
    while x<8:
        num = 99*x
        let_l.append(num)
        num_l.append(num)
        x += 1

class bad_fen(Exception):
    pass

def stock_setup(fen=None,death=False,easy=False):
    
    if death != False:
        stockfish.set_elo_rating(3000)
    if easy != False:
        stockfish.set_elo_rating(900)
    else:
        stockfish.set_elo_rating(1600)
    if fen != None:
        f_t = stockfish.is_fen_valid(fen)
        if f_t != False:
            stockfish.set_fen_position(fen)
        else:
            raise bad_fen

def replacen(piecess, option=None,noquest=None):
    pcc = ''
    for a,b in enumerate(piecess):
        
        pp = pieces_all[a]
        if pp[0] == 'w':
            pcc = pp[1].upper()
        else:
            pcc = pp[1].lower()
        
        for c,d in enumerate(piecess[a]):
            places = d[0]
            roww = d[1]
            ro = row_[roww]
            ro[row_place[places]] = pcc
    for i in all_rows:
        print(i)
    fen = fen_gen(option,noquest=noquest)
    for a in range(8):
            all_rows[a].clear()
            for i in range(8):
                all_rows[a].append('E')
    return fen

def fen_gen(option=None,noquest=None):
    class fen_wrong(Exception):
        pass
    deff = [[],[],[],[],[],[],[],[]]
    for i,h in enumerate(all_rows):
        temp = []
        empty = 0
        row = all_rows[i]
        for a,b in enumerate(row):
            result = 1
            if b == 'E':
                empty +=1
                if empty == 8:
                     result = '8'
                
            if b != 'E':
                if empty > 0:
                    result = f'{b}'
                    empty = 0
                else:
                    result = f'{b}'
            temp.append(result)
        g= 0
        temp_s = ''
        for f in temp:
            
            try:
                g += f
            except:
                if g>0:
                    temp_s += f'{g}{f}'
                else:
                    temp_s += f'{f}'
                g = 0
        if g > 0 :
             temp_s += f'{g}'
             g = 0
        if temp_s == '78':
            temp_s = '8'
        deff[i].append(temp_s)
    a_end = f'{deff[0][0]}/{deff[1][0]}/{deff[2][0]}/{deff[3][0]}/{deff[4][0]}/{deff[5][0]}/{deff[6][0]}/{deff[7][0]}'
    if option != None:
        play = option
    else:
        play = utility.move()
    if noquest == None:
        wc = utility.w_castle()
        bc = utility.b_castle()
    else:
        wc = 'no'
        bc = wc

    now.clear()
    now.append(play)
    
    a_end += f' {play}'
    if wc == 'no':
        a_end += ' '
    else:
        a_end += f' {wc}'
    if bc == 'no':
        pass
    if wc and bc == 'no':
        a_end += '-'
    else:
        a_end += f'{bc}'
    a_end += ' - 1 1'
    if stockfish.is_fen_valid(a_end) == True:
        return a_end
    else:
        print('oops something went wrong with the fen generation please copy and paste your fen')
        fen = input()
        if stockfish.is_fen_valid(fen) == True:
            return a_end
        else:
            raise fen_wrong

def find_place(x, y):
   
    g = []
    l = []
    for kk in let_l:
        g.append(abs(x-kk))
    for kk in num_l:
        l.append(abs(y-kk)) 

    left = let_l[g.index(min(g))]
    top = num_l[l.index(min(l))]
    return left, top

def find_all(img, k=False,option=None,noquest=None):
    temp = []
    hele = []
    value = 0.9
    for nu,i in enumerate(pieces_all):
        imgg = c2(cv2.imread(f'pieces/{i}.png'))
        imgg = cv2.resize(imgg, (block_size,block_size))

        for d in pg.locateAll(imgg, img,confidence=value):
            left, top= find_place(d.left, d.top)
            temp.append(f'{lett[left]}{numm[top]}')
            if k != False:
                cv2.rectangle(img, 
                        (left, top),
                        (left +99, top + 99),
                        (2,23,251), 2
                        )
        tt = list(dict.fromkeys(temp))
        hele.append(tt)
                
        
            
        #print(tt)
        temp.clear()
    fen = replacen(hele, option,noquest=noquest)
    return fen

nig = [0]

def begin(board, fen=False):
    if fen != False and nig[0] == 0:
        ch = utility.sugest()
        if ch == 'y':
            nig[0] = 1
            board = pg.Box(left=404, top=169, width=792, height=792)
        else:
            pass
    if nig[0] == 1:
        board = pg.Box(left=404, top=169, width=792, height=792)
    time.sleep(1)
    screenshot = np.array(pg.screenshot(region=board))
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGBA)
    return screenshot

def create_fen(img=False, option=None,noquest=None):
    fill()
    board_onscreen = board_p()
    hh =  begin(board_onscreen,fen=True)
    clean_img = clean(hh)
    fen = find_all(clean_img,k=img,option=option,noquest=noquest)
    return fen, clean_img

def do_chess():
    pp = {'b':'w','w':'b'}
    while 1:    
        if now[0] == opp[0]:
            fen,img = create_fen(img=True,option=now[0],noquest=True)
        if now[0] != opp[0]:
            fen,img = create_fen(img=False,option=now[0],noquest=False)

        if opp[0] != now[0]:
            
            
            stock_setup(fen)
            print(stockfish.get_board_visual())
            best = stockfish.get_best_move()
            stockfish.make_moves_from_current_position([f'{best}'])
            utility.click(best)
            print(stockfish.get_board_visual())
            print(best)
            now[0] = opp[0]
            
        else:
            stock_setup(fen)
            print(stockfish.get_board_visual())
            cv2.imshow('waiting for input',img)
            cv2.waitKey(0)
            now[0] = pp[now[0]]

def start():
    choise = utility.st()
    if choise == 'c':
        m = utility.default()
        if m == 'y':
            pass
        if m != 'y':
            mode = utility.dif_mode()
            if mode == 'd':
                stock_setup(death=True)
            if mode == 'e':
                stock_setup(easy=True)
        opp.append(utility.op())
        fen, img = create_fen()
        stock_setup(fen=fen)
        do_chess()

    if choise == 'f':
        fen, img = create_fen(img=False) 
        print(fen)



start()
