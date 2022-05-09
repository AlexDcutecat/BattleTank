import pygame
import numpy as np
import random
import time

#游戏战场边框坐标
SCREEN_L=92
SCREEN_T=92
SCREEN_B=508  #172+13*32
SCREEN_R=508

#窗口大小
SCREEN_X=600
SCREEN_Y=600

#难度，范围大于2，数值越低难度越高
leveldifficulty=5

#按键方向列表
direc=[[pygame.K_w,pygame.K_s,pygame.K_d,pygame.K_a],[pygame.K_UP,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_LEFT]]

#按键映射字典
direc1={pygame.K_w:'UP',pygame.K_s:'DOWN',pygame.K_d:'RIGHT',pygame.K_a:'LEFT'}#P1
direc2={pygame.K_UP:'UP',pygame.K_DOWN:'DOWN',pygame.K_RIGHT:'RIGHT',pygame.K_LEFT:'LEFT'}#P2

#按键状态缓冲
dir_key1={pygame.K_w:0,pygame.K_s:0,pygame.K_d:0,pygame.K_a:0}#P1
dir_key2={pygame.K_UP:0,pygame.K_DOWN:0,pygame.K_RIGHT:0,pygame.K_LEFT:0}#P2

#敌人随机运动选择库，下方向多，敌人随机向下移动
direcenemy=['DOWN','UP','RIGHT','LEFT','DOWN','RIGHT','LEFT','DOWN']

#障碍类型
barrier_pool={0:'air',
              1:'wall',2:'wall',3:'wall',4:'wall',5:'wall',6:'wall',7:'wall',8:'wall',
              9:'wall',10:'wall',11:'wall',12:'wall',13:'wall',14:'wall',15:'wall',
              16:'iron',17:'iron',18:'iron',19:'iron',20:'iron',21:'iron',22:'iron',23:'iron',
              24:'iron',25:'iron',26:'iron',27:'iron',28:'iron',29:'iron',30:'iron',#2x2的砖跟铁分别有十五种摆法
              31:'water',
              32:'grass',
              33:'ice'}

#游戏单位长宽
height=32
length=32

#地图(暂时)
tankmap=np.array([[ 0, 0,11, 0, 0,15, 0,15, 0, 0,7, 0, 0],
                  [32, 0, 0, 0, 0, 0,15, 0, 0, 0, 0, 0,32],
                  [ 0, 0, 0,15,32,15,32,15,32,15, 0, 0,15],
                  [15, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0,15],
                  [15,31,31, 0, 0, 0, 0, 0, 0, 0,31,31,15],
                  [ 0, 0,15, 0,30,30,30,30,30, 0,15, 0, 0],
                  [15, 0,15, 0, 0, 0, 0, 0, 0, 0,15, 0,15],
                  [ 0, 0,15,15,15,15,15,15,15,15,15, 0, 0],
                  [ 0, 0,15, 0,15, 0,33, 0,15, 0,15, 0, 0],
                  [30,13,15,15,15,15,15,15,15,15,15,14,30],
                  [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [ 0, 0, 0, 0, 0, 8,12, 4, 0, 0, 0, 0, 0],
                  [ 0, 0, 0, 0, 0,10, 0, 5, 0, 0, 0, 0, 0]])

tankmap_quick_creat={0:0,1:3,2:5,3:12,4:10,5:15,6:18,7:20,8:27,9:25,10:30,11:31,12:32,13:33}

tankmap_mapping=np.array([[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

tankmap_creat=np.array([[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0, 8,12, 4, 0, 0, 0, 0, 0],
                        [ 0, 0, 0, 0, 0,10, 0, 5, 0, 0, 0, 0, 0]])

#敌方坦克难度随机选择库
tankhardlevel=[1,1,1,1,1,2,2,2,3]


#敌人是否包含奖励随机选择库
enemy_bonus=[False,False,False,False,False,True,True,True,True,True,True]


#敌人出生点
enemy_home=np.array([[0,6,12],
                    [0,0,0]])

unbeatable_image_pool={}
unbeatable_image_pool['UP']=pygame.image.load('image/protectframe0.png')
unbeatable_image_pool['DOWN']=pygame.image.load('image/protectframe1.png')

text_image=pygame.image.load('image/letters.png')
text_image_bool={'stage':pygame.rect.Rect(0,0,75,14),'pause':pygame.rect.Rect(0,64,76,14),'gameover':pygame.rect.Rect(0,80,60,30),
                 'B_0':pygame.rect.Rect(0,16,14,14), 'Y_0':pygame.rect.Rect(0,112,14,14), 'W_0':pygame.rect.Rect(0,144,14,14),
                 'B_1':pygame.rect.Rect(15,16,14,14),'Y_1':pygame.rect.Rect(15,112,14,14),'W_1':pygame.rect.Rect(15,144,14,14),
                 'B_2':pygame.rect.Rect(30,16,14,14),'Y_2':pygame.rect.Rect(30,112,14,14),'W_2':pygame.rect.Rect(30,144,14,14),
                 'B_3':pygame.rect.Rect(46,16,14,14),'Y_3':pygame.rect.Rect(46,112,14,14),'W_3':pygame.rect.Rect(46,144,14,14),
                 'B_4':pygame.rect.Rect(62,16,14,14),'Y_4':pygame.rect.Rect(62,112,14,14),'W_4':pygame.rect.Rect(62,144,14,14),
                 'B_5':pygame.rect.Rect(0,32,14,14), 'Y_5':pygame.rect.Rect(0,128,14,14), 'W_5':pygame.rect.Rect(0,160,14,14),
                 'B_6':pygame.rect.Rect(15,32,14,14),'Y_6':pygame.rect.Rect(15,128,14,14),'W_6':pygame.rect.Rect(15,160,14,14),
                 'B_7':pygame.rect.Rect(30,32,14,14),'Y_7':pygame.rect.Rect(30,128,14,14),'W_7':pygame.rect.Rect(30,160,14,14),
                 'B_8':pygame.rect.Rect(46,32,14,14),'Y_8':pygame.rect.Rect(46,128,14,14),'W_8':pygame.rect.Rect(46,160,14,14),
                 'B_9':pygame.rect.Rect(62,32,14,14),'Y_9':pygame.rect.Rect(62,128,14,14),'W_9':pygame.rect.Rect(62,160,14,14),}

ship_image={}
ship_image['p1']=pygame.image.load('image/shipframeO.png')
ship_image['p2']=pygame.image.load('image/shipframeG.png')
ship_image['enemy']=pygame.image.load('image/shipframeW.png')

enemycounter=pygame.image.load('image/enemynum.png')
p1_flag=pygame.image.load('image/1p.png')
p2_flag=pygame.image.load('image/2p.png')
stage_flag=pygame.image.load('image/flag.png')
playercounter=pygame.image.load('image/playerlifenum.png')

#奖励池
bonus_pool=['1up','grenade','gun','star','shovel','timer','ship','helmet']

#核心周围的坐标池
homewall_pos=[(11,5),(11,6),(11,7),(12,5),(12,7)]

pygame.mixer.init()

channel1=pygame.mixer.Channel(1)
channel2=pygame.mixer.Channel(2)
channel3=pygame.mixer.Channel(3)
channel4=pygame.mixer.Channel(4)

#
sound_list1={'gamestart':'gamestart.ogg','gameover':'gameover.ogg','attack':'attack.wav','pause':'pause.wav'}
sound_list2={'background':'background.ogg','count':'count.wav','misc':'misc.wav'}
sound_list3={'explosion':'explosion.ogg', 'bonus':'bonus.ogg','life':'life.wav'}
sound_list4={'move':'move.wav','hit_frame':'hit_frame.wav','hit_tank':'hit_tank.wav','hit_wall':'hit_wall.wav'}


def play_sound(s,con=0):
    if s in sound_list1.keys():
        if channel1.get_busy()==True:
            pass
        else:
            sound=pygame.mixer.Sound('sound1/{}'.format(sound_list1[s]))
            channel1.play(sound,con)
    elif s in sound_list2.keys():
        if channel2.get_busy()==True:
            pass
        else:
            sound=pygame.mixer.Sound('sound1/{}'.format(sound_list2[s]))
            channel2.play(sound,con)
    elif s in sound_list3.keys():
        if channel3.get_busy()==True:
            pass
        else:
            sound=pygame.mixer.Sound('sound1/{}'.format(sound_list3[s]))
            channel3.play(sound,con)
    elif s in sound_list4.keys():
        if channel4.get_busy()==True:
            pass
        else:
            sound=pygame.mixer.Sound('sound1/{}'.format(sound_list4[s]))
            channel4.play(sound,con)

def stop_allsound():
    channel1.stop()
    channel2.stop()
    channel3.stop()
    channel4.stop()
    
def stop_mostsound():
    channel2.stop()
    channel3.stop()
    channel4.stop()

#对象基类
class BaseItem(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen=screen
        self.live=True
        
    def display(self):
        if self.live is True:
            self.image = self.images[self.direction]
            self.screen.blit(self.image,self.rect)

#文字类
class Text(BaseItem):
    def __init__(self,screen,string,color='B',pos=[0,0]):
        #string:'stage','pause','0','9',color:'W','B','Y'
        super(Text,self).__init__(screen)
        if len(string)==1:
            self.image=text_image.subsurface(text_image_bool['{}_{}'.format(color,string)])
        else:
            self.image=text_image.subsurface(text_image_bool[string])
        self.pos=pos
        self.rect=self.image.get_rect()
        #self.rect.left,self.rect.top=self.pos[:]
        
    def display(self):
        if self.live is True:
            self.rect.left,self.rect.top=self.pos[:]
            self.screen.blit(self.image,self.rect)
            
#分数类
class Score(BaseItem):
    def __init__(self,screen,pos,score_value=100):
        super(Score,self).__init__(screen)
        self.pos=pos
        self.image=pygame.image.load('image/score{}.png'.format(score_value))
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=self.pos[:]
        self.display_step=35
        
    def display(self):
        if self.live is True:
            if self.display_step>0:
                self.display_step-=1
                self.screen.blit(self.image,self.rect)
            else:
                self.display_step=30
                self.live =False


#奖励类
class Bonus(BaseItem):
    def __init__(self,screen):
        super(Bonus,self).__init__(screen)
        self.pos=[SCREEN_L+random.randint(2,11)*32-8,SCREEN_T+random.randint(2,11)*32-8]
        self.reveal_timer=time.time()
        self.glimmer=0
        self.bonus_type=random.choice(bonus_pool)
        self.direction='UP'
        self.images={}
        self.images['UP']=pygame.image.load('image/bonus_{}.png'.format(self.bonus_type))
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.width=self.rect.width//2
        self.rect.height=self.rect.height//2
        self.rect.left,self.rect.top = self.pos[:]
        
    def isLive(self):
        if self.reveal_timer <= time.time()-20.0:
            self.live=False
            
    def display(self):
        if self.live is True:
            if self.reveal_timer <= time.time()-15.0:#执行闪烁效果
                if self.glimmer <= 10:
                    self.glimmer+=1
                    self.images['UP']=pygame.image.load('image/empty.png')
                    self.image = self.images[self.direction]
                    self.screen.blit(self.image,(self.rect.left-8,self.rect.top-8))
                elif 10<self.glimmer<=20:
                    self.glimmer+=1
                    self.images['UP']=pygame.image.load('image/bonus_{}.png'.format(self.bonus_type))
                    self.image = self.images[self.direction]
                    self.screen.blit(self.image,(self.rect.left-8,self.rect.top-8))
                else:
                    self.glimmer=0
            else:
                self.image = self.images[self.direction]
                self.screen.blit(self.image,(self.rect.left-8,self.rect.top-8))
