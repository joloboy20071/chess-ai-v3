import pyautogui as pg
import time

def click(a):
    x = {'a':0,'b':99,'c':198,'d':297,'e':396,'f':495,'g':594,'h':693}
    y = {'8':0,'7':99,'6':198,'5':297,'4':396,'3':495,'2':594,'1':693}
    lefta = x[a[0]] + 404 +45
    topa = y[a[1]] + 169 + 45
    leftb = x[a[2]] + 404 +45
    topb = y[a[3]] + 169 + 45

    pg.click(lefta,topa,button='left')
    time.sleep(1)
    pg.click(leftb,topb,button='left')

def st():
    h = {'Chess ai':'c','Generate fen':'f'}
    n = pg.confirm(text='what do you want?', title='begining', buttons=['Chess ai','Generate fen'])
    return h[n]

def op():
    h = {'White':'w','Black':'b'}
    n = pg.confirm(text='Who is the opponent?', title='opponent', buttons=['White', 'Black'])
    return h[n]

def sugest():
    h = {'Yes':'y','No':'n'}
    n = pg.confirm(text='when using fen use suggested config for 1920x1080', title='sugest', buttons=['Yes', 'No'])
    return h[n]

def default():
    h = {'Yes':'y','No':'n'}
    n = pg.confirm(text='would you like to use the default mode for the ai?', title='default', buttons=['Yes', 'No'])
    return h[n]

def dif_mode():
    h = {'Death':'d','Easy':'e'}
    n = pg.confirm(text='Death or easy mode?', title='Death or easy', buttons=['Death', 'Easy'])
    return h[n]


def move():
    h = {'White':'w','Black':'b'}
    n = pg.confirm(text='Who\'s move is it', title='Move', buttons=['White', 'Black'])
    return h[n]

def w_castle():
    h = {'King queen':'KQ', 'King':'K', 'Queen':'Q', 'Can\'t':'no'}
    n = pg.confirm(text='Can white castle', title='castle', buttons=['King queen', 'King', 'Queen', 'Can\'t'])
    return h[n]

def b_castle():
    h = {'King queen':'kq', 'King':'k', 'Queen':'q', 'Can\'t':'no'}
    n = pg.confirm(text='Can Black castle', title='castle', buttons=['King queen', 'King', 'Queen', 'Can\'t'])
    return h[n]





