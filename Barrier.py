from GlobalVariable import *

#核心
class Eagle(BaseItem):
    def __init__(self,screen):
        super(Eagle,self).__init__(screen)
        self.pos=[SCREEN_L+6*32,SCREEN_T+12*32]
        self.direction='UP'
        self.defeat=False
        self.images={}
        self.images['UP']=pygame.image.load('image/eagle.png')
        self.images['DOWN']=pygame.image.load('image/deadeagle.png')
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = self.pos[:]

#障碍基类
class Barrier(BaseItem):
    def __init__(self,screen,x,y):
        super().__init__(screen)
        self.direction="UP"
        self.pos=[x,y]
        self.type=None

#砖墙类(小)
class Wall(Barrier):
    def __init__(self,screen,x,y):
        super(Wall,self).__init__(screen,x,y)
        self.images={}
        self.images['UP']=pygame.image.load('image/brick_small.png')
        self.image=self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=self.pos[:]
        
class HomeWall(Wall):
    def __init__(self,screen,x,y):
        super(HomeWall,self).__init__(screen,x,y)
        self.images={}
        self.images['UP']=pygame.image.load('image/brick_small.png')
        self.images['DOWN']=pygame.image.load('image/iron_small.png')
        self.image=self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=self.pos[:]
        self.isiron=False
        self.change_timer=None
        self.image_change_flag = 18
    
    def change_to_iorn(self):
        self.isiron=True
        self.direction='DOWN'
        self.change_timer=time.time()
    
    def ischangetime(self):
        if self.change_timer<=time.time()-20:
            self.isiron=False
            self.direction='UP'
    
    def changedir(self):
        if self.direction == 'UP':
            self.direction = 'DOWN'
        else:
            self.direction = 'UP'
    
    def display(self):
        if self.live is True:
            if self.isiron==True:
                if self.change_timer<=time.time()-15.0:
                    if self.image_change_flag == 0:
                        self.image_change_flag = 18
                        self.changedir()
                    else:
                        self.image_change_flag -= 1
            self.image = self.images[self.direction]
            self.screen.blit(self.image,self.rect)
        
        

#铁墙类(小)
class Iron(Barrier):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)
        self.type=2
        self.images={}
        self.images['UP']=pygame.image.load('image/iron_small.png')
        self.image=self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=self.pos[:]

#水类        
class Water(Barrier):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)
        self.type=3
        self.image_change_flag=18
        self.images={}
        self.images['UP']=pygame.image.load('image/water0.png')
        self.images['DOWN']=pygame.image.load('image/water1.png')
        self.image=self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=self.pos[:]
    
    def display(self):
        if self.live is True:
            if self.image_change_flag == 0:
                self.image_change_flag = 18
                self.changedir()
            else:
                self.image_change_flag -= 1
            self.image = self.images[self.direction]
            self.screen.blit(self.image,self.rect)
        
    def changedir(self):
        if self.direction == 'UP':
            self.direction = 'DOWN'
        else:
            self.direction = 'UP'  

#草类
class Grass(Barrier):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)
        self.type=4
        self.images={}
        self.images['UP']=pygame.image.load('image/grass.png')
        self.image=self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=self.pos[:]

#冰类
class Ice(Barrier):
    def __init__(self,screen,x,y):
        super().__init__(screen,x,y)
        self.type=5
        self.images={}
        self.images['UP']=pygame.image.load('image/ice.png')
        self.image=self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=self.pos[:]

#边框
class Frame(BaseItem):
    def __init__(self,screen,x,y,width,height):
        super(Frame,self).__init__(screen)
        #self.pos=[x,y]
        self.rect=pygame.rect.Rect(x,y,width,height)
