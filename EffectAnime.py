from GlobalVariable import *
from Main import Main
#出生闪烁状态
class RebornStar(BaseItem):
    def __init__(self,screen,pos):
        super(RebornStar,self).__init__(screen)
        self.pos=pos#2元素列表
        self.step=0
        self.timer=0
        self.images=[]
        for i in range(4):
            self.images.append(pygame.image.load('image/star{}.png'.format(i)))
        self.rect=self.images[0].get_rect()
        self.rect.left=pos[0]
        self.rect.top=pos[1]
    
    #坦克出生动画
    def display(self):
        if self.live:
            if self.step < 4:
                if self.timer > 0:
                    self.screen.blit(self.images[self.step],self.rect)
                    self.timer-=1
                else:
                    self.step+=1
                    self.timer=4
            elif self.step < 8:
                if self.timer > 0:
                    self.screen.blit(self.images[self.step-4],self.rect)
                    self.timer-=1
                else:
                    self.step+=1
                    self.timer=4
            elif self.step < 12:
                if self.timer > 0:
                    self.screen.blit(self.images[self.step-8],self.rect)
                    self.timer-=1
                else:
                    self.step+=1
                    self.timer=4
            elif self.step < 16:
                if self.timer > 0:
                    self.screen.blit(self.images[self.step-12],self.rect)
                    self.timer-=1
                else:
                    self.step+=1
                    self.timer=4
            else:
                self.live=False    


#爆炸类
class Blast(BaseItem):
    def __init__(self,screen,pos,boomtype=1,score_type=0):
        super(Blast,self).__init__(screen)
        self.pos=pos
        self.step=0
        self.type=boomtype  #两类，第一类为子弹击中障碍跟边框的爆炸
                            #第二类为子弹击败坦克后坦克的爆炸
        self.images=[pygame.image.load('image/boom0.png'),
                     pygame.image.load('image/boom1.png'),
                     pygame.image.load('image/boom2.png'),
                     pygame.image.load('image/boom3.png'),
                     pygame.image.load('image/boom4.png'),]
        self.rect=self.images[0].get_rect()
        self.rect2=self.images[3].get_rect()
        self.rect.left=pos[0]-8
        self.rect.top=pos[1]-8
        self.rect2.left=pos[0]-16
        self.rect2.top=pos[1]-16
        self.score=score_type
        
    #爆炸动画
    def display(self):
        if self.live:
            if self.step < 5:
                self.screen.blit(self.images[0],self.rect)
                self.step+=1
            elif self.step < 10:
                self.screen.blit(self.images[1],self.rect)
                self.step+=1
            elif self.step < 15:
                self.screen.blit(self.images[2],self.rect)
                self.step+=1
            if self.type==2:
                if self.step < 20:
                    self.screen.blit(self.images[3],self.rect2)
                    self.step+=1
                elif self.step < 25:
                    self.screen.blit(self.images[4],self.rect2)
                    self.step+=1
                else:
                    self.step=0
                    if self.score!=0:
                        Main.score.add(Score(self.screen,self.pos,self.score))
                    self.live=False
    
