### version: V1.1
### author: LUWic
### date: 2022/6/16

import pygame
import random
import time

class ShowBackground:
    def show_background(self,x,y,screen,width):
        image = pygame.transform.scale(
            pygame.image.load('./images/background.png'),
            (width,width)
        )
        rect = image.get_rect()
        rect.x = x*width
        rect.y = y*width
        screen.blit(image,rect)
        return rect

class ShowMine:
    def show_mine(self,x,y,screen,width):
        image = pygame.transform.scale(
            pygame.image.load('./images/mine.png'),
            (width,width)
        )
        rect = image.get_rect()
        rect.x = x*width
        rect.y = y*width
        screen.blit(image,rect)
        return rect

class HiddenRect:
    def hidden_rect(self,x,y,screen,width):
        image = pygame.transform.scale(
            pygame.image.load('./images/rect.png'),
            (width,width)
        )
        rect = image.get_rect()
        rect.x = x
        rect.y = y
        screen.blit(image,rect)
        return rect

class Number:
    def __init__(self,num):
        images = ['one','two','three','four','five','six','seven','eight']
        self.image = images[num-1]
    def number(self,x,y,screen,width):
        image = pygame.transform.scale(
            pygame.image.load('./images/'+self.image+'.png'),
            (width,width)
        )
        rect = image.get_rect() 
        rect.x = x*width
        rect.y = y*width
        screen.blit(image,rect)
        return rect

class Flag:
    def flag(self,x,y,screen,width):
        image = pygame.transform.scale(
            pygame.image.load('./images/flag.png'),
            (width,width)
        )
        rect = image.get_rect()
        rect.x = x*width
        rect.y = y*width
        screen.blit(image,rect)
        return rect

class Doubt:
    def doubt(self,x,y,screen,width):
        image = pygame.transform.scale(
            pygame.image.load('./images/doubt.png'),
            (width,width)
        )
        rect = image.get_rect()
        rect.x = x*width
        rect.y = y*width
        HiddenRect().hidden_rect(rect.x,rect.y,screen,width)
        screen.blit(image,rect)
        return rect


def create_hidde_rect(hidden_rect,screen,width,rect_row_count):
    y = 0
    while y <= 600:
        x = 0
        while x <= 600: 
            hidden_rect.hidden_rect(x,y,screen,width)
            x += width
        y += width
    return [(x,y) for x in range(rect_row_count) for y in range(rect_row_count)]

def create_mine(num, rect_row_count):
    mines = set()
    while len(mines)<=num:
        mines.add( (random.randint(0,rect_row_count-1),random.randint(0,rect_row_count-1)) )
    return mines

def is_mine(x,y,mines):
    for mx,my in mines:
        if x == mx and y == my:
            return (x,y)

def has_rects(x,y,rect_row_count):
    rects = [(x-1,y),(x+1,y),(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y+1),(x,y+1),(x+1,y+1)]
    has_rects = []
    for rect in rects:
        if not ((rect[0]<0)or(rect[0]>rect_row_count-1)or(rect[1]<0)or(rect[1]>rect_row_count-1)):
            has_rects.append(rect)
    return has_rects

def has_mines(x,y,mines,rect_row_count):
    rects = has_rects(x,y,rect_row_count)
    num = 0
    for r in rects:
        if r in mines:
            num+=1
    return num

def extend_find_mines(x,y,mines,rect_row_count):
    three_tuple = []
    num = has_mines(x,y,mines,rect_row_count)
    if num:
        three_tuple.append((x,y,num))
    else:
        not_mines = [(x,y)]
        kill = []
        while len(not_mines):
            xy = not_mines[0]
            rects = [
                (xy[0],xy[1]),(xy[0]-1,xy[1]),(xy[0]+1,xy[1]),
                (xy[0],xy[1]-1),(xy[0],xy[1]+1),(xy[0]-1,xy[1]-1),
                (xy[0]+1,xy[1]+1),(xy[0]+1,xy[1]-1),(xy[0]-1,xy[1]+1)
            ]
            has_rects = []
            for rect in rects:
                if not ((rect[0]<0)or(rect[0]>rect_row_count-1)or(rect[1]<0)or(rect[1]>rect_row_count-1)):
                    has_rects.append(rect)
            for x,y in has_rects:
                num = has_mines(x,y,mines,rect_row_count)
                if not ((x==xy[0])and(y==xy[1])):
                    if not((x,y) in not_mines) and not((x,y) in kill):
                        if not num:
                            not_mines.append((x,y))
                three_tuple.append((x,y,num))
            kill.append(not_mines.pop(0))
    return three_tuple

def is_end(hidden_rect,flags,doubts,mines):
    if len(hidden_rect)+len(flags)+len(doubts) == len(mines):
        num=0
        for end in hidden_rect+flags+doubts:
            if end in mines:
                num +=1
        if num == len(mines):
            return False
    return True

def event_process(event,mines,hidden_rect,flags,doubts,screen,width,rect_row_count):
    if event.button == 1:
        pos = pygame.mouse.get_pos()
        x_id = pos[0]//width
        y_id = pos[1]//width
        if (x_id,y_id) in hidden_rect:
            if (xy := is_mine(x_id,y_id,mines)):
                show_mine = ShowMine()
                show_mine.show_mine(x_id,y_id,screen,width)
                return False
            else:
                mine_info = extend_find_mines(x_id,y_id,mines,rect_row_count)
                for x,y,mines_num in mine_info:
                    try:
                        hidden_rect.remove((x,y))
                    except:
                        pass
                    else:
                        if not mines_num:
                            show_background = ShowBackground()
                            show_background.show_background(x,y,screen,width)
                        else:
                            number = Number(mines_num)
                            number.number(x,y,screen,width)
    
    elif event.button == 3:
        pos = pygame.mouse.get_pos()
        x_id = pos[0]//width
        y_id = pos[1]//width
        if (xy:=(x_id,y_id)) in hidden_rect:
            flag = Flag()
            flag.flag(x_id,y_id,screen,width)
            flags.append(xy)
            hidden_rect.remove(xy)
        elif xy in flags:
            doubt = Doubt()
            doubt.doubt(x_id,y_id,screen,width)
            doubts.append(xy)
            flags.remove(xy)
        elif xy in doubts:
            rect = HiddenRect()
            rect.hidden_rect(x_id*width,y_id*width,screen,width)
            hidden_rect.append(xy)
            doubts.remove(xy)
    return True


class Main:
    def __init__(self):

        # 设置
        self.rect_row_count = 20        # 一行含多少个块
        self.rect_width = 20            # 每个块的大小
        self.mines_count = self.rect_row_count**2//8           # 雷的数量

        self.window_size = (self.rect_width*self.rect_row_count,self.rect_width*self.rect_row_count)

        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_icon(pygame.image.load("./ico.ico"))
        pygame.display.set_caption('扫雷')
        self.screen.fill((255,255,255))

        pygame.event.clear()

        hidden_rect = HiddenRect()
        self.hidden_rect = create_hidde_rect(hidden_rect,self.screen,self.rect_width,self.rect_row_count)
        self.mines = list(create_mine(self.mines_count-1,self.rect_row_count))
        self.flags = []
        self.doubts = []

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not (event_process(event,self.mines,self.hidden_rect,self.flags,self.doubts,self.screen,self.rect_width,self.rect_row_count)):
                        pygame.display.update()
                        time.sleep(1)
                        return True
                elif event.type == pygame.QUIT:
                    return False

            if not(is_end(self.hidden_rect,self.flags,self.doubts,self.mines)):
                pygame.display.update()
                time.sleep(1)
                return False

            pygame.display.update()

flag = True
while flag:
    main = Main()
    flag = main.main()