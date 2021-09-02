from GlobalVariable import *
from Barrier import HomeWall
from Bullet import *
from EffectAnime import *
import time
import random

#坦克类
class Tank(BaseItem):
    def __init__(self,screen,x,y,hard):
        #screen,x,y,hard
        super().__init__(screen)
        self.direction='UP'
        self.speed=1  #坦克移动速度
        self.pos=[x,y]
        self.stop=False
        self.change=True #更改动画贴图flag
        self.state=None  #坦克状态
        self.on_ice=False  #坦克是否在冰上
        self.slideflag=10  #坦克在冰上滑动计数器
        self.collideflag = False  #坦克碰撞flag
        self.hardlevel = hard  #坦克强度 1 2 3 一共三级
        self.lifes = 1 #耐打能力，默认为1
        self.image_chage_timer=time.time()
        self.unbeatable=False  #无敌状态
        self.unbeat_timer=0  #无敌计时器
        self.unbeat_limit=5  #无敌计时上限
        self.effect=RebornStar(self.screen,self.pos)  #出生状态动画类
        self.unbeatable_image=None  #无敌贴图
        self.freeze=False  #被冻结flag
        self.freeze_timer=None  #冻结计时器
        self.can_get_bonus=True  #能否获得道具
        self.fire_power=1  #坦克火力，默认为1
        self.ship=False
        self.id=None
    
    def set_unbeatable_state(self):
        if self.unbeatable==False:
            self.unbeatable=1
            self.unbeat_timer=time.time()
        
    def isunbeatable(self):
        if self.unbeat_timer<=time.time()-self.unbeat_limit:
            self.unbeatable=False
    
    def display(self):
        if self.live is True:
            if self.ship == True:
                self.screen.blit(ship_image[self.id],self.rect)
            if self.unbeatable_image!=None:
                self.screen.blit(self.unbeatable_image,self.rect)
            self.image = self.images[self.direction]
            self.screen.blit(self.image,self.rect)
    
    #移动
    def move(self,Main):#,timer
        
        #更改坦克贴图，产生动画效果
        if self.image_chage_timer <= time.time()-0.05:
            if self.unbeatable == True:
                if self.unbeatable_image == unbeatable_image_pool['DOWN']:
                    self.unbeatable_image=unbeatable_image_pool['UP']
                else:
                    self.unbeatable_image=unbeatable_image_pool['DOWN']
            else:
                self.unbeatable_image=None
            self.image_chage_timer = time.time()
            self.change = not self.change
            self.images = self.image_pool[self.change]
        
        #移动
        if self.stop == False:
            if self.freeze == False:
                self.pos = [self.rect.left,self.rect.top][:] #记录坐标
                if self.direction == 'UP': 
                    self.rect.top -= self.speed
                if self.direction == 'DOWN':
                    self.rect.top += self.speed
                if self.direction == 'RIGHT':
                    self.rect.left += self.speed
                if self.direction == 'LEFT':
                    self.rect.left -= self.speed
            elif self.freeze_timer<=time.time()-5.0:
                self.freeze=False
        else:
            if (self.pos[0]-SCREEN_L)-(self.pos[0]-SCREEN_L)//16*16 > 8:
                self.pos[0]=((self.pos[0]-SCREEN_L)//16+1)*16+SCREEN_L
            else:
                self.pos[0]=((self.pos[0]-SCREEN_L)//16)*16+SCREEN_L
            if (self.pos[1]-SCREEN_T)-(self.pos[1]-SCREEN_T)//16*16 > 8:
                self.pos[1]=((self.pos[1]-SCREEN_T)//16+1)*16+SCREEN_T
            else:
                self.pos[1]=((self.pos[1]-SCREEN_T)//16)*16+SCREEN_T
        
    
    def get_bonus(self,bonus,Main):
        
        if bonus.bonus_type=='1up':
            play_sound('life')
            Main.score.add(Score(self.screen,bonus.pos,500))
        elif bonus.bonus_type=='ship':
            play_sound('bonus')
            self.ship=True
            Main.score.add(Score(self.screen,bonus.pos,200))
        elif bonus.bonus_type=='star':
            play_sound('bonus')
            if self.fire_power+1>=4:
                self.fire_power=4
            else:
                self.fire_power+=1
            self.bulletspeed = 6
            if self in Main.mytanklist:
                self.lifes=self.fire_power
                self.changeImage()
            Main.score.add(Score(self.screen,bonus.pos,200))
        elif bonus.bonus_type=='gun':
            play_sound('bonus')
            self.fire_power=4
            self.bulletspeed = 6
            if self in Main.mytanklist:
                self.lifes=self.fire_power
                self.changeImage()
            Main.score.add(Score(self.screen,bonus.pos,400))
        elif bonus.bonus_type=='shovel':
            play_sound('bonus')
            if self in Main.mytanklist:
                Main.homewalls.empty()
                for (i,j) in homewall_pos:
                    c0=tankmap[i][j]>>3
                    c1=(tankmap[i][j]>>2)&1
                    c2=(tankmap[i][j]>>1)&1
                    c3=tankmap[i][j]&1
                    if c0:
                        Main.homewalls.add(HomeWall(self.screen,SCREEN_T+j*32+16,SCREEN_L+i*32+16))
                    if c1:
                        Main.homewalls.add(HomeWall(self.screen,SCREEN_T+j*32,SCREEN_L+i*32+16))
                    if c2:
                        Main.homewalls.add(HomeWall(self.screen,SCREEN_T+j*32+16,SCREEN_L+i*32))
                    if c3:
                        Main.homewalls.add(HomeWall(self.screen,SCREEN_T+j*32,SCREEN_L+i*32))
                for wall in Main.homewalls:
                    wall.change_to_iorn()
            else:
                Main.homewalls.empty()
            Main.score.add(Score(self.screen,bonus.pos,200))
        elif bonus.bonus_type=='helmet':
            play_sound('bonus')
            self.set_unbeatable_state()
            Main.score.add(Score(self.screen,bonus.pos,200))
        elif bonus.bonus_type=='grenade':
            play_sound('explosion')
            if self in Main.mytanklist:
                for e in Main.enemylist:
                    e.live=False
                    Main.blastlist.add(Blast(self.screen,e.pos,2))
                #Main.enemylist.empty()
            elif self in Main.enemylist:
                for e in Main.mytanklist:
                    e.live=False
                    Main.blastlist.add(Blast(self.screen,e.pos,2))
                #Main.mytanklist.empty()
            Main.score.add(Score(self.screen,bonus.pos,200))
        elif bonus.bonus_type=='timer':
            play_sound('bonus')
            if self in Main.mytanklist:
                for e in Main.enemylist:
                    if e.freeze == False:
                        e.freeze=True
                        e.freeze_timer=time.time()
            else:
                for e in Main.mytanklist:
                    if e.freeze == False:
                        e.freeze=True
                        e.freeze_timer=time.time()
            Main.score.add(Score(self.screen,bonus.pos,200))

    def iscollide(self,Main):
        #检测坦克之间的碰撞，碰撞即停，以及防止粘住
        enelist=pygame.sprite.Group()
        for ene in Main.mytanklist:
            if ene is self:
                pass
            else:
                enelist.add(ene)
        tanklist=pygame.sprite.spritecollide(self,enelist,False)#
        if tanklist:
            self.collideflag=True
            self.rect.left,self.rect.top=self.pos[:]
        else:
            pass
            #self.collideflag=False
        
        #检测与坦克的碰撞，在出生时如果重叠二者都会粘住(未解决)
        enelist=pygame.sprite.Group()
        for ene in Main.enemylist:
            if ene is self:
                pass
            else:
                enelist.add(ene)
        tanklist=pygame.sprite.spritecollide(self,enelist,False)#
        if tanklist:
            self.collideflag=True
            #self.stop=True
            self.rect.left,self.rect.top=self.pos[:]
        else:
            pass
            #self.collideflag=False
        
        #与各种障碍之间的碰撞检测
        #与墙壁的碰撞
        tanklist = pygame.sprite.spritecollide(self,Main.walls,False)
        if tanklist:
            self.rect.left,self.rect.top = self.pos[:]
            self.collideflag = True
        #与家周围墙壁的碰撞
        tanklist = pygame.sprite.spritecollide(self,Main.homewalls,False)
        if tanklist:
            self.rect.left,self.rect.top = self.pos[:]
            self.collideflag = True
        #与铁墙的碰撞
        tanklist = pygame.sprite.spritecollide(self,Main.irons,False)
        if tanklist:
            self.rect.left,self.rect.top = self.pos[:]
            self.collideflag = True
        #与水的碰撞
        if self.ship==False:
            tanklist = pygame.sprite.spritecollide(self,Main.water,False)
            if tanklist:
                self.rect.left,self.rect.top = self.pos[:]
                self.collideflag = True
        #与边框的碰撞
        tanklist = pygame.sprite.spritecollide(self,Main.worldframelist,False)
        if tanklist:
            self.rect.left,self.rect.top = self.pos[:]
            self.collideflag = True
        #与核心的碰撞
        tanklist = pygame.sprite.spritecollide(self,Main.eaglelist,False)
        if tanklist:
            self.rect.left,self.rect.top = self.pos[:]
            self.collideflag = True
        #吃到奖励
        if self.can_get_bonus==True:#通过此flag开关不同阵营的坦克获得道具的能力
            tanklist = pygame.sprite.spritecollide(self,Main.bonus,False)
            if tanklist:
                for bonus in Main.bonus:
                    self.get_bonus(bonus,Main)
                Main.bonus.empty()
        #检测是否在冰上
        tanklist = pygame.sprite.spritecollide(self,Main.ices,False)
        if tanklist:
            self.on_ice = True
        else:
            self.on_ice = False

#友方坦克类
class myTank(Tank):
    def __init__(self,screen,x,y,hard,tankid='p1'):
        super().__init__(screen,x,y,hard)
        self.fire_power=1
        self.id=tankid
        self.bulletspeed = 8 if self.fire_power>=2 else 6
        self.tanklives=3
        self.images = {}
        self.images1 = {}
        self.images2 = {}
        self.image_pool = {}
        self.images1['UP'] = pygame.image.load('image/{}U0_1.png'.format(self.id))
        self.images1['DOWN'] = pygame.image.load('image/{}D0_1.png'.format(self.id))
        self.images1['LEFT'] = pygame.image.load('image/{}L0_1.png'.format(self.id))
        self.images1['RIGHT'] = pygame.image.load('image/{}R0_1.png'.format(self.id))
        self.images2['UP'] = pygame.image.load('image/{}U0_2.png'.format(self.id))
        self.images2['DOWN'] = pygame.image.load('image/{}D0_2.png'.format(self.id))
        self.images2['LEFT'] = pygame.image.load('image/{}L0_2.png'.format(self.id))
        self.images2['RIGHT'] = pygame.image.load('image/{}R0_2.png'.format(self.id))
        self.image_pool[True] = self.images1
        self.image_pool[False] = self.images2
        self.images = self.image_pool[self.change]
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = self.pos[:]
    
    #改变方向
    def changeDir(self,ddir):
        self.stop=False
        if self.freeze==False:
            if self.direction != ddir:
                self.direction = ddir
                self.image = self.images[self.direction]
                self.rect = self.image.get_rect()
                self.rect.left,self.rect.top = self.pos[:]
    
    #开火
    def fire(self):
        return myMissile(self)
    
    
    #判断方向按键是否松开，以及松开时冰上的处理
    def isStop(self,dir_key):
        if self.id=='p1':
            if (dir_key1[pygame.K_s] == 0 and dir_key1[pygame.K_w] == 0
                and dir_key1[pygame.K_a] == 0 and dir_key1[pygame.K_d] == 0):
                if self.on_ice == True:
                    if self.slideflag > 0:
                        self.slideflag -= 1
                        self.stop = False
                    else:
                        self.stop = True
                else:
                        self.stop = True
            else:
                self.slideflag = 10
        else:
            if (list(dir_key2.values())[0] == 0 and list(dir_key2.values())[1] == 0
                and list(dir_key2.values())[2] == 0 and list(dir_key2.values())[3] == 0):
                if self.on_ice == True:
                    if self.slideflag > 0:
                        self.slideflag -= 1
                        self.stop = False
                    else:
                        self.stop = True
                else:
                        self.stop = True
            else:
                self.slideflag = 10
        
    def changeImage(self):
        if self.lifes>0:
            self.images1['UP'] = pygame.image.load('image/{}U{}_1.png'.format(self.id,self.lifes-1))
            self.images1['DOWN'] = pygame.image.load('image/{}D{}_1.png'.format(self.id,self.lifes-1))
            self.images1['LEFT'] = pygame.image.load('image/{}L{}_1.png'.format(self.id,self.lifes-1))
            self.images1['RIGHT'] = pygame.image.load('image/{}R{}_1.png'.format(self.id,self.lifes-1))
            self.images2['UP'] = pygame.image.load('image/{}U{}_2.png'.format(self.id,self.lifes-1))
            self.images2['DOWN'] = pygame.image.load('image/{}D{}_2.png'.format(self.id,self.lifes-1))
            self.images2['LEFT'] = pygame.image.load('image/{}L{}_2.png'.format(self.id,self.lifes-1))
            self.images2['RIGHT'] = pygame.image.load('image/{}R{}_2.png'.format(self.id,self.lifes-1))

#敌方坦克类
class enemyTank(Tank):
    def __init__(self,screen,x=0,y=0,enetype=1,hard=1):
        #screen,x,y,tpye{1,2,3,4},hard{1,2,3}
        super().__init__(screen,x,y,hard)
        self.step = 0 #140-leveldifficulty*10  #随机状态计数flag,设置为0使其在出生后即移动
        self.direction = 'DOWN'
        self.id='enemy'
        self.speed=1
        self.type = enetype #坦克类型，一共四种
        self.contain_bonus = random.choice(enemy_bonus)
        self.lifes = self.hardlevel#敌方坦克挨打能力 与坦克难度等级有关
        self.firetimer=time.time()  #开火间隔计时器
        self.unbeat_limit=5
        if self.type==2:
            self.speed = 2
        elif self.type==3:
            self.fire_power+=1
        elif self.type==4 and self.lifes<3:
            self.lifes+=1
        self.bulletspeed = 6 if self.fire_power >= 2 else 4
        self.can_get_bonus=True
        self.dirchange_timer=time.time()
        self.images = {}
        self.images1 = {}
        self.images2 = {}
        self.image_pool = {}
        if self.contain_bonus == True:
            self.images1['UP'] = pygame.image.load('image/enemy{}_{}U_1.png'.format(self.type,4))
            self.images1['DOWN'] = pygame.image.load('image/enemy{}_{}D_1.png'.format(self.type,4))
            self.images1['LEFT'] = pygame.image.load('image/enemy{}_{}L_1.png'.format(self.type,4))
            self.images1['RIGHT'] = pygame.image.load('image/enemy{}_{}R_1.png'.format(self.type,4))
            self.images2['UP'] = pygame.image.load('image/enemy{}_{}U_2.png'.format(self.type,4))
            self.images2['DOWN'] = pygame.image.load('image/enemy{}_{}D_2.png'.format(self.type,4))
            self.images2['LEFT'] = pygame.image.load('image/enemy{}_{}L_2.png'.format(self.type,4))
            self.images2['RIGHT'] = pygame.image.load('image/enemy{}_{}R_2.png'.format(self.type,4))
        else:
            self.images1['UP'] = pygame.image.load('image/enemy{}_{}U_1.png'.format(self.type,self.lifes))
            self.images1['DOWN'] = pygame.image.load('image/enemy{}_{}D_1.png'.format(self.type,self.lifes))
            self.images1['LEFT'] = pygame.image.load('image/enemy{}_{}L_1.png'.format(self.type,self.lifes))
            self.images1['RIGHT'] = pygame.image.load('image/enemy{}_{}R_1.png'.format(self.type,self.lifes))
            self.images2['UP'] = pygame.image.load('image/enemy{}_{}U_2.png'.format(self.type,self.lifes))
            self.images2['DOWN'] = pygame.image.load('image/enemy{}_{}D_2.png'.format(self.type,self.lifes))
            self.images2['LEFT'] = pygame.image.load('image/enemy{}_{}L_2.png'.format(self.type,self.lifes))
            self.images2['RIGHT'] = pygame.image.load('image/enemy{}_{}R_2.png'.format(self.type,self.lifes))
        self.image_pool[True] = self.images1
        self.image_pool[False] = self.images2
        self.images = self.image_pool[self.change]
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = self.pos[:]
        
    
    #随机改变方向，设置移动flag
    def changeDir(self):
        if self.freeze == False:
            if self.collideflag is True or self.dirchange_timer<=(time.time()-random.gauss(5.4,1)):
                self.dirchange_timer=time.time()
                self.direction=random.choice(direcenemy)
                self.image=self.images[self.direction]
                self.rect=self.image.get_rect()
                self.rect.left,self.rect.top=self.pos[:]
                self.collideflag=False
                self.stop=False
            
    def changeImage(self):
        self.images1['UP'] = pygame.image.load('image/enemy{}_{}U_1.png'.format(self.type,self.lifes))
        self.images1['DOWN'] = pygame.image.load('image/enemy{}_{}D_1.png'.format(self.type,self.lifes))
        self.images1['LEFT'] = pygame.image.load('image/enemy{}_{}L_1.png'.format(self.type,self.lifes))
        self.images1['RIGHT'] = pygame.image.load('image/enemy{}_{}R_1.png'.format(self.type,self.lifes))
        self.images2['UP'] = pygame.image.load('image/enemy{}_{}U_2.png'.format(self.type,self.lifes))
        self.images2['DOWN'] = pygame.image.load('image/enemy{}_{}D_2.png'.format(self.type,self.lifes))
        self.images2['LEFT'] = pygame.image.load('image/enemy{}_{}L_2.png'.format(self.type,self.lifes))
        self.images2['RIGHT'] = pygame.image.load('image/enemy{}_{}R_2.png'.format(self.type,self.lifes))
#         self.image_pool[True] = self.images1
#         self.image_pool[False] = self.images2
    
    def fire(self):
        return enemyMissile(self)
