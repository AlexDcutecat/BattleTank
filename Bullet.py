from GlobalVariable import *
from EffectAnime import *
from time import time


#子弹类
class Missile(BaseItem):
    def __init__(self,tank):
        super().__init__(tank.screen)
        self.pos=[tank.rect.left+length/2-8,tank.rect.top+height/2-8]
        self.direction=tank.direction
        self.images={}
        self.images['UP']=pygame.image.load('image/bulletU.png')
        self.images['DOWN']=pygame.image.load('image/bulletD.png')
        self.images['LEFT']=pygame.image.load('image/bulletL.png')
        self.images['RIGHT']=pygame.image.load('image/bulletR.png')
        self.image=self.images[self.direction]
        self.rect=self.image.get_rect()
        self.rect.left,self.rect.top=self.pos[:]
        self.speed=tank.bulletspeed
        self.power=tank.fire_power
        
    #子弹移动    
    def move(self,Main):
        if self.direction == 'UP':
            if self.rect.top <= SCREEN_T:
                if self in Main.mybulletlist1 or self in Main.mybulletlist2:
                    play_sound('hit_frame')
                self.rect.top = SCREEN_T
                self.live=False
                Main.blastlist.add(Blast(self.screen,self.pos,1))
                return
            self.rect.top -= self.speed
        if self.direction == 'DOWN':
            if self.rect.bottom >= SCREEN_B:
                if self in Main.mybulletlist1 or self in Main.mybulletlist2:
                    play_sound('hit_frame')
                self.rect.bottom = SCREEN_B
                self.live=False
                Main.blastlist.add(Blast(self.screen,self.pos,1))
                return
            self.rect.top += self.speed
        if self.direction == 'RIGHT':
            if self.rect.right >= SCREEN_R:
                if self in Main.mybulletlist1 or self in Main.mybulletlist2:
                    play_sound('hit_frame')
                self.rect.right = SCREEN_R
                self.live=False
                Main.blastlist.add(Blast(self.screen,self.pos,1))
                return
            self.rect.left += self.speed
        if self.direction == 'LEFT':
            if self.rect.left <= SCREEN_L:
                if self in Main.mybulletlist1 or self in Main.mybulletlist2:
                    play_sound('hit_frame')
                self.rect.left = SCREEN_L
                self.live=False
                Main.blastlist.add(Blast(self.screen,self.pos,1))
                return
            self.rect.left -= self.speed
        self.pos=self.rect.left,self.rect.top#记录坐标
    
    #击中障碍
    def hit_item(self,Main):
        #击中砖墙时，使砖墙消失
        en=pygame.sprite.spritecollide(self,Main.walls,False)
        if en:
            for e in en:
                #play_sound('hit_wall')
                e.live=False
                Main.walls.remove(e)
                Main.blastlist.add(Blast(self.screen,self.pos,1))
                if self in Main.mybulletlist1:
                    play_sound('hit_wall')
                    Main.mybulletlist1.remove(self)
                elif self in Main.mybulletlist2:
                    play_sound('hit_wall')
                    Main.mybulletlist2.remove(self)
                else:
                    Main.enemybulletlist.remove(self)
        
        #击中铁墙时
        en=pygame.sprite.spritecollide(self,Main.irons,False)
        if en:
            for e in en:
                if self.power >= 4:
                    play_sound('hit_wall')
                    e.live=False
                    Main.irons.remove(e)
                Main.blastlist.add(Blast(self.screen,self.pos,1))
                if self in Main.mybulletlist1:
                    play_sound('hit_frame')
                    Main.mybulletlist1.remove(self)
                elif self in Main.mybulletlist2:
                    play_sound('hit_frame')
                    Main.mybulletlist2.remove(self)
                else:
                    Main.enemybulletlist.remove(self)
        
        
        en=pygame.sprite.spritecollide(self,Main.homewalls,False)
        if en:
            for e in en:
                if e.isiron==True:
                    if self.power >= 4:
                        e.live=False
                        Main.homewalls.remove(e)
                else:
                    e.live=False
                    Main.homewalls.remove(e)
                    
                Main.blastlist.add(Blast(self.screen,self.pos,1))
                if self in Main.mybulletlist1:
                    Main.mybulletlist1.remove(self)
                elif self in Main.mybulletlist2:
                    Main.mybulletlist2.remove(self)
                else:
                    Main.enemybulletlist.remove(self)
        
        #击中核心时
        en=pygame.sprite.spritecollide(self,Main.eaglelist,False)
        if en:
            for e in en:
                e.defeat=False
                e.direction='DOWN'
                #Main.blastlist.add(Blast(self.screen,self.pos,1))
                if self in Main.mybulletlist1:
                    Main.mybulletlist1.remove(self)
                elif self in Main.mybulletlist2:
                    Main.mybulletlist2.remove(self)
                else:
                    Main.enemybulletlist.remove(self)

#友方子弹类
class myMissile(Missile):
    def __init__(self,tank):
        super(myMissile,self).__init__(tank)
        
    def hit_enemy(self,Main):
        #击中敌人
        en=pygame.sprite.spritecollide(self,Main.enemylist,False)
        if en:
            for e in en:
                if e.effect.live is False:
                    if e.unbeatable==False:
                        if e.ship==False:
                            if e.contain_bonus == True:
                                e.contain_bonus=False
                                Main.bonus.empty()
                                Main.bonus.add(Bonus(self.screen))
                            e.lifes -= self.power
                            if e.lifes > 0:
                                play_sound('hit_tank')
                                e.changeImage()
                            else:
                                play_sound('explosion')
                                e.live=False
                                #Main.enemylist.remove(e)
                                Main.blastlist.add(Blast(self.screen,self.pos,1))
                                Main.blastlist.add(Blast(self.screen,e.pos,2,e.type*100))
                        else:
                            play_sound('hit_frame')
                            e.ship=False
                    Main.mybulletlist1.remove(self)
                    Main.mybulletlist2.remove(self)
        
        #与敌方子弹对消
        en=pygame.sprite.spritecollide(self,Main.enemybulletlist,True)
        if en:
            for e in en:
                e.live=False
                Main.enemybulletlist.remove(e)
            #Main.blastlist.add(Blast(self.screen,self.pos))  #爆炸效果
            Main.mybulletlist1.remove(self)
            Main.mybulletlist2.remove(self)

#敌方子弹类
class enemyMissile(Missile):
    def __init__(self,tank):
        super(enemyMissile,self).__init__(tank)
        
    def hit_enemy(self,Main):
        #击中敌人(玩家)
        en=pygame.sprite.spritecollide(self,Main.mytanklist,False)
        if en:
            for e in en:
                if e.effect.live is False:
                    if  e.unbeatable==False:
                        if e.ship==False:
                            e.lifes -= 1
                            e.fire_power=e.lifes
                            e.bulletspeed = 6 if e.fire_power>=2 else 4
                            e.changeImage()
                            if e.lifes <= 0:
                                play_sound('explosion')
                                e.live=False
                                Main.mytanklist.remove(e)
                                Main.blastlist.add(Blast(self.screen,self.pos,1))
                                Main.blastlist.add(Blast(self.screen,e.pos,2))
                        else:
                            play_sound('hit_tank')
                            e.ship=False
                    Main.enemybulletlist.remove(self)
