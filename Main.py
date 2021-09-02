from GlobalVariable import *
from Barrier import *
from Tank import *
import time
import random
from sys import exit

class Main():
    
#key_buffer={'p1':{'UP':0,'DOWN':0,'LEFT':0,'RIGHT':0,'A':0,'B':0,'START':0,'SELECT':0},
#                'p2':{'UP':0,'DOWN':0,'LEFT':0,'RIGHT':0,'A':0,'B':0,'START':0,'SELECT':0}}#未用
    
    worldframelist = pygame.sprite.Group()
    
    time1=pygame.time.Clock()

    mybulletlist1 = pygame.sprite.Group()
    mybulletlist2 = pygame.sprite.Group()
    
    enemybulletlist = pygame.sprite.Group()

    blastlist = pygame.sprite.Group()

    mytanklist = pygame.sprite.Group()
    tank1=None
    tank2=None
    
    eaglelist = pygame.sprite.Group()
    eagle=None
    
    enemylist=pygame.sprite.Group()
    
    walls=pygame.sprite.Group()
    homewalls=pygame.sprite.Group()
    irons=pygame.sprite.Group()
    grass=pygame.sprite.Group()
    water=pygame.sprite.Group()
    ices=pygame.sprite.Group()
    rebornstarlist=pygame.sprite.Group()
    bonus=pygame.sprite.Group()
    score=pygame.sprite.Group()
    
    tanktimer=time.time()
    enemy_creat_timer=time.time()
    firetimer=time.time()
    
    enemytanknum=20
    enemytankcount=20
    
    process=1  #游戏画面显示进程
    game_process=1  #游戏内在逻辑进程  与前者区别在于开始前的序幕与游玩过程在同一画面显示进程里 方便音乐播放以及按键操作多态性
    
    menu_step=104  #菜单动画计数器
    curtain_step=52  #幕布动画计数器
    kill_all_step=200
    is_first_stage=1
    
    menu=pygame.image.load('image/menu.png')
    score_s=pygame.image.load('image/board_s.png')
    score_d=pygame.image.load('image/board_d.png')
    pointer=pygame.image.load('image/p1R0_1.png')
    pointer_pos=[3,1]  #大致坐标
    
    creat_brick=pygame.image.load('image/brick_small.png')
    creat_iron=pygame.image.load('image/iron_small.png')
    creat_grass=pygame.image.load('image/grass.png')
    creat_ice=pygame.image.load('image/ice.png')
    creat_water=pygame.image.load('image/water0.png')
    creat_eagle=pygame.image.load('image/eagle.png')
    
    creat_step=50
    creat_move_step=[25,25,25,25]
    creat_move_timegap=14
    creat_pointer=pygame.image.load('image/p1U0_1.png')
    creat_pointer_pressbuf={'UP':0,'DOWN':0,'LEFT':0,'RIGHT':0,'B':0,'A':0}
    creat_pointer_num=0
    creat_pointer_pos=[0,0]
    creat_stage_num=1
    
    playernum=1
    game_pause=False
    game_start=False
    game_curtain_start=False
    
    current_stage=1
    
    #创建地图上各个对象
    def draw_map(self):
        for i in range(13):
            for j in range(13):
                if barrier_pool[tankmap[i][j]] == 'wall': #1-15
                    c0=tankmap[i][j]>>3
                    c1=(tankmap[i][j]>>2)&1
                    c2=(tankmap[i][j]>>1)&1
                    c3=tankmap[i][j]&1
                    if (i,j) in homewall_pos:#(i,j)==(11,5) or (i,j)==(11,6) or (i,j)==(11,7) or (i,j)==(12,5) or (i,j)==(12,7):
                        if c0:
                            Main.homewalls.add(HomeWall(self.screen,SCREEN_T+j*32+16,SCREEN_L+i*32+16))
                        if c1:
                            Main.homewalls.add(HomeWall(self.screen,SCREEN_T+j*32,SCREEN_L+i*32+16))
                        if c2:
                            Main.homewalls.add(HomeWall(self.screen,SCREEN_T+j*32+16,SCREEN_L+i*32))
                        if c3:
                            Main.homewalls.add(HomeWall(self.screen,SCREEN_T+j*32,SCREEN_L+i*32))
                    else:
                        if c0:
                            Main.walls.add(Wall(self.screen,SCREEN_T+j*32+16,SCREEN_L+i*32+16))
                        if c1:
                            Main.walls.add(Wall(self.screen,SCREEN_T+j*32,SCREEN_L+i*32+16))
                        if c2:
                            Main.walls.add(Wall(self.screen,SCREEN_T+j*32+16,SCREEN_L+i*32))
                        if c3:
                            Main.walls.add(Wall(self.screen,SCREEN_T+j*32,SCREEN_L+i*32))
                if barrier_pool[tankmap[i][j]] == 'iron': #1-15
                    c0=(tankmap[i][j]-15)>>3
                    c1=((tankmap[i][j]-15)>>2)&1
                    c2=((tankmap[i][j]-15)>>1)&1
                    c3=(tankmap[i][j]-15)&1
                    if c0:
                        Main.irons.add(Iron(self.screen,SCREEN_T+j*32+16,SCREEN_L+i*32+16))
                    if c1:
                        Main.irons.add(Iron(self.screen,SCREEN_T+j*32,SCREEN_L+i*32+16))
                    if c2:
                        Main.irons.add(Iron(self.screen,SCREEN_T+j*32+16,SCREEN_L+i*32))
                    if c3:
                        Main.irons.add(Iron(self.screen,SCREEN_T+j*32,SCREEN_L+i*32))
#                 if barrier_pool[tankmap[i][j]] == 'iron':#16
#                     Main.irons.add(Iron(self.screen,SCREEN_T+j*32,SCREEN_L+i*32))
                if barrier_pool[tankmap[i][j]] == 'water':#17
                    Main.water.add(Water(self.screen,SCREEN_T+j*32,SCREEN_L+i*32))
                if barrier_pool[tankmap[i][j]] == 'grass':#18
                    Main.grass.add(Grass(self.screen,SCREEN_T+j*32,SCREEN_L+i*32))
                if barrier_pool[tankmap[i][j]] == 'ice':#19
                    Main.ices.add(Ice(self.screen,SCREEN_T+j*32,SCREEN_L+i*32))
    
    #清除每个组里的对象
    def remove_all(self):
        Main.walls.empty()
        Main.homewalls.empty()
        Main.irons.empty()
        Main.grass.empty()
        Main.mytanklist.empty()
        Main.enemylist.empty()
        Main.rebornstarlist.empty()
        Main.enemybulletlist.empty()
        Main.mybulletlist1.empty()
        Main.mybulletlist2.empty()
        Main.water.empty()
        Main.ices.empty()
        Main.eaglelist.empty()
        Main.blastlist.empty()
        Main.bonus.empty()
        stop_allsound()
    
    
    def event_get1(self):
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                exit()
            if event.type is pygame.KEYDOWN:
                #选择
                if event.key in direc[0]:
                    if event.key==pygame.K_w:
                        Main.pointer_pos[1]-=1
                        if Main.pointer_pos[1]<1:
                            Main.pointer_pos[1]=3
                    elif event.key==pygame.K_s:
                        Main.pointer_pos[1]+=1
                        if Main.pointer_pos[1]>3:
                            Main.pointer_pos[1]=1
                 
                #按退格键确认
                if event.key is pygame.K_BACKSPACE:
                    Main.game_start=True

    #接收事件
    def event_get2(self):
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                exit()
            if event.type is pygame.KEYDOWN:
                #移动
                if event.key in direc[0]:
                    Main.tank1.changeDir(direc1[event.key])
                    dir_key1[event.key]=1
                    
                if event.key in direc[1]:
                    Main.tank2.changeDir(direc2[event.key])
                    dir_key2[event.key]=1

                #按J发射子弹
                if event.key is pygame.K_j and Main.tank1.live and len(Main.mybulletlist1)<=1 and Main.tank1.effect.live is False:
                    play_sound('attack')
                    Main.mybulletlist1.add(Main.tank1.fire())
                
                if event.key is pygame.K_SLASH and Main.tank2.live and len(Main.mybulletlist2)<=1 and Main.tank2.effect.live is False:
                    play_sound('attack')
                    Main.mybulletlist2.add(Main.tank2.fire())
                
                if event.key is pygame.K_j and Main.game_process==2:
                    Main.current_stage+=1
                    if Main.current_stage>=100:
                        Main.current_stage=1
                if event.key is pygame.K_k and Main.game_process==2:
                    Main.current_stage-=1
                    if Main.current_stage<=0:
                        Main.current_stage=99
                
                #按退格键暂停游戏
                if event.key is pygame.K_BACKSPACE:
                    if Main.game_process==3:
                        play_sound('pause')
                        Main.game_pause=not Main.game_pause
                    if Main.game_process==2:
                        play_sound('gamestart')
                        Main.game_curtain_start=True
                        Main.game_process=3

                #按数字1键复活
                if event.key is pygame.K_1:
                    if Main.tank1.live == False:
                        Main.tank1=myTank(self.screen,SCREEN_L+4*32,SCREEN_T+12*32,1)
                        Main.tank1.set_unbeatable_state()
                        Main.rebornstarlist.add(Main.tank1.effect)
                        Main.mytanklist.add(Main.tank1)
                    if Main.playernum==2:
                        if Main.tank2.live == False:
                            Main.tank2=myTank(self.screen,SCREEN_L+8*32,SCREEN_T+12*32,1,'p2')
                            Main.tank2.set_unbeatable_state()
                            Main.rebornstarlist.add(Main.tank2.effect)
                            Main.mytanklist.add(Main.tank2)
                
                if event.key is pygame.K_p:
                    
                    print(Main.enemytankcount)
                    print(len(Main.enemylist))
                
                if event.key is pygame.K_0:
                    if Main.eagle.live == False:
                        pass

            if event.type is pygame.KEYUP:
                #按键松开改变按键状态 
                if event.key in direc[0]:
                    dir_key1[event.key]=0
                    for i in direc[0]:
                        if dir_key1[i] != 0 and i != event.key:
                            Main.tank1.changeDir(direc1[i])
                    
                if event.key in direc[1]:
                    dir_key2[event.key]=0
                    for i in direc[1]:
                        if dir_key2[i] != 0 and i != event.key:
                            Main.tank2.changeDir(direc2[i])
                            
                if direc[1][0]==direc[1][1]==direc[1][2]==direc[1][3]==direc[0][0]==direc[0][1]==direc[0][2]==direc[0][3]==0:
                    channel4.stop()
    
    def event_get3(self):
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                exit()
            if event.type is pygame.KEYDOWN:
                if event.key in direc[0]:
                    if event.key==pygame.K_w:
                        Main.creat_pointer_pressbuf['UP']=1
                        Main.creat_pointer_pos[1] = Main.creat_pointer_pos[1]-1 if Main.creat_pointer_pos[1]-1>=0 else 0
                    if event.key==pygame.K_s:
                        Main.creat_pointer_pressbuf['DOWN']=1
                        Main.creat_pointer_pos[1] = Main.creat_pointer_pos[1]+1 if Main.creat_pointer_pos[1]+1<=12 else 12
                    if event.key==pygame.K_a:
                        Main.creat_pointer_pressbuf['LEFT']=1
                        Main.creat_pointer_pos[0] = Main.creat_pointer_pos[0]-1 if Main.creat_pointer_pos[0]-1>=0 else 0
                    if event.key==pygame.K_d:
                        Main.creat_pointer_pressbuf['RIGHT']=1
                        Main.creat_pointer_pos[0] = Main.creat_pointer_pos[0]+1 if Main.creat_pointer_pos[0]+1<=12 else 12
                if event.key == pygame.K_j:
                    Main.creat_pointer_pressbuf['B']=1
                    if tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]==0 and Main.creat_pointer_num!=0:
                        tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]=Main.creat_pointer_num
                    elif tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]==0 and Main.creat_pointer_num==0:
                        Main.creat_pointer_num+=1
                        if Main.creat_pointer_num>=14:
                            Main.creat_pointer_num=0
                        tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]=Main.creat_pointer_num
                    elif tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]!=0:# and Main.creat_pointer_num==0:
                        Main.creat_pointer_num=tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]
                        Main.creat_pointer_num+=1
                        if Main.creat_pointer_num>=14:
                            Main.creat_pointer_num=0
                        tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]=Main.creat_pointer_num
                if event.key == pygame.K_k:
                    Main.creat_pointer_pressbuf['A']=1
                    if tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]==0 and Main.creat_pointer_num!=0:
                        tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]=Main.creat_pointer_num
                    elif tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]==0 and Main.creat_pointer_num==0:
                        Main.creat_pointer_num-=1
                        if Main.creat_pointer_num<0:
                            Main.creat_pointer_num=13
                        tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]=Main.creat_pointer_num
                    elif tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]!=0:# and Main.creat_pointer_num==0:
                        Main.creat_pointer_num=tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]
                        Main.creat_pointer_num-=1
                        if Main.creat_pointer_num<0:
                            Main.creat_pointer_num=13
                        tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]=Main.creat_pointer_num
                if event.key is pygame.K_BACKSPACE:
                    Main.process=1
                    Main.game_process=1
                if event.key == pygame.K_p:
                    with open(r'map/{0:02}'.format(Main.creat_stage_num),'wb')as f:
                        try:
                            pickle.dump(tankmap_creat,f)
                            print('地图{0}存储完毕,存储位置map/{0:02}'.format(Main.creat_stage_num))
                        except:
                            print('写入异常')
                if event.key == pygame.K_n:
                    Main.creat_stage_num-=1
                    if Main.creat_stage_num<1:
                        Main.creat_stage_num=99
                if event.key == pygame.K_m:
                    Main.creat_stage_num+=1
                    if Main.creat_stage_num>99:
                        Main.creat_stage_num=1
                if event.key == pygame.K_y:
                    for i in range(13):
                        for j in range(13):
                            tankmap_mapping[i][j]=0
                        
            if event.type is pygame.KEYUP:
                if event.key in direc[0]:
                    if event.key==pygame.K_w:
                        Main.creat_pointer_pressbuf['UP']=0
                    if event.key==pygame.K_s:
                        Main.creat_pointer_pressbuf['DOWN']=0
                    if event.key==pygame.K_a:
                        Main.creat_pointer_pressbuf['LEFT']=0
                    if event.key==pygame.K_d:
                        Main.creat_pointer_pressbuf['RIGHT']=0
                if event.key==pygame.K_j:
                    Main.creat_pointer_pressbuf['B']=0
                if event.key==pygame.K_k:
                    Main.creat_pointer_pressbuf['A']=0
                    
    #显示对象，以及执行对象行为
    def object_display(self):
        if Main.game_pause==True:
            stop_mostsound()
            return
        
        self.screen.fill((0x7f,0x7f,0x7f))
        pygame.draw.rect(self.screen,(1,1,1),pygame.Rect(SCREEN_L,SCREEN_T,SCREEN_R-SCREEN_L,SCREEN_B-SCREEN_T))
        
        Main.eagle.display()
        
        enebuf=[0,1,2]
        #ene=[]
        #同时最多4个敌人
        if len(Main.enemylist) < 3 and Main.enemytanknum>0:
            if Main.enemylist:
                for e in Main.enemylist:
                    if e.pos[0] <= SCREEN_L+32 and e.pos[1] <= SCREEN_Y+32: #地图上(0,0)坐标方格内有坦克时不新建坦克
                        enebuf[0] = 3
                        break
                for e in Main.enemylist:
                    if SCREEN_L+5*32 <= e.pos[0] <=SCREEN_L + 7*32 and e.pos[1] <= SCREEN_Y+32:#地图上(6,0)坐标方格内有坦克时不新建坦克
                        enebuf[1] = 3
                        break
                for e in Main.enemylist:
                    if SCREEN_L+11*32 <= e.pos[0] and e.pos[1] <= SCREEN_Y+32:#地图上(12,0)坐标方格内有坦克时不新建坦克
                        enebuf[2] = 3
                        break

                for e in Main.mytanklist:
                    if e.pos[0] <= SCREEN_L+32 and e.pos[1] <= SCREEN_Y+32: #地图上(0,0)坐标方格内有坦克时不新建坦克
                        enebuf[0] = 3
                        break
                for e in Main.mytanklist:
                    if SCREEN_L+5*32 <= e.pos[0] <=SCREEN_L + 7*32 and e.pos[1] <= SCREEN_Y+32:#地图上(6,0)坐标方格内有坦克时不新建坦克
                        enebuf[1] = 3
                        break
                for e in Main.mytanklist:
                    if SCREEN_L+11*32 <= e.pos[0] and e.pos[1] <= SCREEN_Y+32:#地图上(12,0)坐标方格内有坦克时不新建坦克
                        enebuf[2] = 3
                        break
            if Main.enemy_creat_timer<time.time()-random.gauss(2.1,0.3):
                Main.enemy_creat_timer=time.time()
                try:
                    Main.enemylist.add(enemyTank(self.screen,
                                                enemy_home[0][random.choice(enebuf)]*32+SCREEN_L,
                                                random.choice(enemy_home[1])*32+SCREEN_T,
                                                random.randint(1,4),
                                                random.choice(tankhardlevel)))
                    Main.enemytanknum-=1
                    for e in Main.enemylist:
                        Main.rebornstarlist.add(e.effect)
                except IndexError:
                    pass
        
        for wall in Main.walls:
            if wall.live:
                wall.display()
            else:
                Main.walls.remove(wall)
        
        for wall in Main.homewalls:
            if wall.live:
                if wall.isiron==True:
                    wall.ischangetime()
                wall.display()
            else:
                Main.walls.remove(wall)
        
        for iron in Main.irons:
            if iron.live:
                iron.display()
            else:
                Main.irons.remove(iron)
        
        for water in Main.water:
            if water.live:
                water.display()
        
        
        for ice in Main.ices:
            if ice.live:
                ice.display()
            else:
                Main.ices.remove(ice)
            
        for score in Main.score:
            if score.live:
                score.display()
            else:
                Main.score.remove(score)

        for blast in Main.blastlist:
            if blast.live:
                blast.display()
            else:
                Main.blastlist.remove(blast)

        for tank in Main.mytanklist:
            if tank.live:
                if tank.effect.live is False:
                    if tank.unbeatable==True:
                        tank.isunbeatable()
                    if tank.id=='p2':
                        tank.isStop(dir_key2)
                    else:
                        tank.isStop(dir_key1)
                    tank.move(Main)#Main.tanktimer
                    tank.iscollide(Main)
                    tank.display()
            else:
                Main.mytanklist.remove(tank)

        for bullet in Main.mybulletlist1:
            if bullet.live is True:
                bullet.display()
                bullet.hit_enemy(Main)
                bullet.hit_item(Main)
                bullet.move(Main)
            else:
                Main.mybulletlist1.remove(bullet) 
                
        for bullet in Main.mybulletlist2:
            if bullet.live is True:
                bullet.display()
                bullet.hit_enemy(Main)
                bullet.hit_item(Main)
                bullet.move(Main)
            else:
                Main.mybulletlist2.remove(bullet)

        for enemy in Main.enemylist:
            if enemy.live is True: #对象是否存活
                if enemy.effect.live is False:  #对象是否处于出生状态
                    if enemy.firetimer <= time.time() - random.gauss(leveldifficulty,1.3):
                        enemy.firetimer=time.time()
                        Main.enemybulletlist.add(enemy.fire())
                    if enemy.unbeatable==True:
                        enemy.isunbeatable()
                    enemy.move(Main)#Main.tanktimer,
                    enemy.iscollide(Main)
                    enemy.changeDir()
                    enemy.display()
            else:
                Main.enemylist.remove(enemy)
                Main.enemytankcount-=1
                
        if Main.enemylist:
            if channel2.get_busy():
                pass
            else:
                play_sound('background',-1)
        else:
            channel2.stop()

        for bullet in Main.enemybulletlist:
            if bullet.live is True:
                bullet.display()
                bullet.hit_enemy(Main)
                bullet.hit_item(Main)
                bullet.move(Main)
            else:
                Main.enemybulletlist.remove(bullet) 
        
        for star in Main.rebornstarlist:
            if star.live:
                star.display()
            else:
                Main.rebornstarlist.remove(star)
                
        for bonus in Main.bonus:
            bonus.isLive()
            if bonus.live:
                bonus.display()
            else:
                Main.bonus.remove(bonus)
                
        for grass in Main.grass:
            if grass.live:
                grass.display()
            else:
                Main.irons.remove(grass)
        
        self.print_UI()
                
        #pygame.display.update()
    
    def menu_display(self):
        self.screen.fill((0x7f,0x7f,0x7f))
        pygame.draw.rect(self.screen,(1,1,1),pygame.Rect(SCREEN_L,SCREEN_T,SCREEN_R-SCREEN_L,SCREEN_B-SCREEN_T))
        if Main.menu_step>=0:
            self.screen.blit(Main.menu,(SCREEN_L,SCREEN_T+4*Main.menu_step))
            self.screen.blit(Main.pointer,
                             (SCREEN_L+Main.pointer_pos[0]*32,SCREEN_T+196+Main.pointer_pos[1]*27+4*Main.menu_step))
            Main.menu_step-=1
        else:
            self.screen.blit(Main.menu,(SCREEN_L,SCREEN_T))
            self.screen.blit(Main.pointer,(SCREEN_L+Main.pointer_pos[0]*32,SCREEN_T+196+Main.pointer_pos[1]*27))
        pygame.draw.rect(self.screen,(0x7f,0x7f,0x7f),pygame.Rect(SCREEN_L,SCREEN_B,SCREEN_R-SCREEN_L,SCREEN_Y-SCREEN_B))#将画面下部分遮盖起来
        pygame.display.update()
        
    def score_display(self):
        self.screen.fill((0x7f,0x7f,0x7f))
        pygame.draw.rect(self.screen,(1,1,1),pygame.Rect(SCREEN_L,SCREEN_T,SCREEN_R-SCREEN_L,SCREEN_B-SCREEN_T))
        if Main.playernum==1:
            self.screen.blit(Main.score_s,(SCREEN_L,SCREEN_T))
        else:
            self.screen.blit(Main.score_d,(SCREEN_L,SCREEN_T))
        pygame.display.update()
    
    def print_UI(self):
        en=0
        if Main.enemytanknum>0:
            for i in range(Main.enemytanknum//2+1 if Main.enemytanknum<=20 else 11):
                for j in range(2):
                    en+=1
                    self.screen.blit(enemycounter,pygame.Rect(SCREEN_R+10+j*16,SCREEN_T+i*16,16,16))
                    if en == Main.enemytanknum:
                        break
                if en == Main.enemytanknum:
                    break
        self.screen.blit(p1_flag,pygame.Rect(SCREEN_R+10,(SCREEN_T+SCREEN_B)/2,32,32))
        self.screen.blit(playercounter,pygame.Rect(SCREEN_R+10,(SCREEN_T+SCREEN_B)/2+32,16,16))
        self.screen.blit(p2_flag,pygame.Rect(SCREEN_R+10,(SCREEN_T+SCREEN_B)/2+64,32,32))
        self.screen.blit(playercounter,pygame.Rect(SCREEN_R+10,(SCREEN_T+SCREEN_B)/2+96,16,16))
        self.screen.blit(stage_flag,pygame.Rect(SCREEN_R+10,(SCREEN_T+SCREEN_B)/2+128,32,32))
    
    def text_init(self):
        self.text_stage=Text(self.screen,'stage','B',(150+SCREEN_L,201+SCREEN_T))
        self.text_B={0:Text(self.screen,'0','B'),10:Text(self.screen,'0','B'),
                     1:Text(self.screen,'1','B'),11:Text(self.screen,'1','B'),
                     2:Text(self.screen,'2','B'),12:Text(self.screen,'2','B'),
                     3:Text(self.screen,'3','B'),13:Text(self.screen,'3','B'),
                     4:Text(self.screen,'4','B'),14:Text(self.screen,'4','B'),
                     5:Text(self.screen,'5','B'),15:Text(self.screen,'5','B'),
                     6:Text(self.screen,'6','B'),16:Text(self.screen,'6','B'),
                     7:Text(self.screen,'7','B'),17:Text(self.screen,'7','B'),
                     8:Text(self.screen,'8','B'),18:Text(self.screen,'8','B'),
                     9:Text(self.screen,'9','B'),19:Text(self.screen,'9','B'),}
        self.text_W={0:Text(self.screen,'0','W'),10:Text(self.screen,'0','W'),
                     1:Text(self.screen,'1','W'),11:Text(self.screen,'1','W'),
                     2:Text(self.screen,'2','W'),12:Text(self.screen,'2','W'),
                     3:Text(self.screen,'3','W'),13:Text(self.screen,'3','W'),
                     4:Text(self.screen,'4','W'),14:Text(self.screen,'4','W'),
                     5:Text(self.screen,'5','W'),15:Text(self.screen,'5','W'),
                     6:Text(self.screen,'6','W'),16:Text(self.screen,'6','W'),
                     7:Text(self.screen,'7','W'),17:Text(self.screen,'7','W'),
                     8:Text(self.screen,'8','W'),18:Text(self.screen,'8','W'),
                     9:Text(self.screen,'9','W'),19:Text(self.screen,'9','W'),}
    
    def text_numdisplay(self,num,color='B',pos=[0,0]):
        if color=='B':
            if num//10==num%10:
                self.text_B[num//10+10].pos=pos
                self.text_B[num%10].pos=pos[0]+16,pos[1]
                self.text_B[num//10+10].display()
                self.text_B[num%10].display()
            self.text_B[num//10].pos=pos
            self.text_B[num%10].pos=pos[0]+16,pos[1]
            self.text_B[num//10].display()
            self.text_B[num%10].display()
        if color=='W':
            if num//10==num%10:
                self.text_W[num//10+10].pos=pos
                self.text_W[num%10].pos=pos[0]+16,pos[1]
                self.text_W[num//10+10].display()
                self.text_W[num%10].display()
            self.text_W[num//10].pos=pos
            self.text_W[num%10].pos=pos[0]+16,pos[1]
            self.text_W[num//10].display()
            self.text_W[num%10].display()
        
    
    def set_all(self):
        self.draw_map()
        #self.text_init()
        
        Main.tank1 = myTank(self.screen,SCREEN_L+4*32,SCREEN_T+12*32,1)
        Main.tank1.set_unbeatable_state()
        Main.mytanklist.add(Main.tank1)
        Main.rebornstarlist.add(Main.tank1.effect)
        
        if Main.playernum==2:
            Main.tank2 = myTank(self.screen,SCREEN_L+8*32,SCREEN_T+12*32,1,'p2')
            Main.tank2.set_unbeatable_state()
            Main.mytanklist.add(Main.tank2)
            Main.rebornstarlist.add(Main.tank2.effect)
        
        Main.eagle = Eagle(self.screen)
        Main.eaglelist.add(Main.eagle)
        
        #添加边框                                 left     top       width     height
        Main.worldframelist.add(Frame(self.screen,0,SCREEN_T,SCREEN_L,SCREEN_B-SCREEN_T))
        Main.worldframelist.add(Frame(self.screen,SCREEN_L,0,SCREEN_R-SCREEN_L,SCREEN_T))
        Main.worldframelist.add(Frame(self.screen,SCREEN_R,SCREEN_T,SCREEN_X-SCREEN_R,SCREEN_B-SCREEN_T))
        Main.worldframelist.add(Frame(self.screen,SCREEN_L,SCREEN_B,SCREEN_R-SCREEN_L,SCREEN_Y-SCREEN_B))
        
        Main.enemy_creat_timer=time.time()
    
    def curtain(self):
        if Main.is_first_stage==True:
            if Main.game_curtain_start==True:
                if Main.curtain_step>=0:
                    
                    pygame.draw.rect(self.screen,(0x7f,0x7f,0x7f),pygame.Rect(SCREEN_L,SCREEN_T,SCREEN_R-SCREEN_L,
                                                                        (SCREEN_B-SCREEN_T)/2-(52-Main.curtain_step)*4))
                    pygame.draw.rect(self.screen,(0x7f,0x7f,0x7f),pygame.Rect(SCREEN_L,
                                                                           (SCREEN_B-SCREEN_T)/2+SCREEN_T+(52-Main.curtain_step)*4,
                                                                           SCREEN_R-SCREEN_L,
                                                                           (SCREEN_B-SCREEN_T)/2-(52-Main.curtain_step)*4))
                    
                    Main.curtain_step-=1
                else:
                    pass
                    
            else:
                pygame.draw.rect(self.screen,(0x7f,0x7f,0x7f),pygame.Rect(SCREEN_L,SCREEN_T,SCREEN_R-SCREEN_L,(SCREEN_B-SCREEN_T)/2))
                pygame.draw.rect(self.screen,(0x7f,0x7f,0x7f),pygame.Rect(SCREEN_L,(SCREEN_B-SCREEN_T)/2+SCREEN_T,
                                                                    SCREEN_R-SCREEN_L,(SCREEN_B-SCREEN_T)/2))
        else:
            if Main.curtain_step>=0:
                pygame.draw.rect(self.screen,(0x7f,0x7f,0x7f),pygame.Rect(SCREEN_L,SCREEN_T,SCREEN_R-SCREEN_L,
                                                                    (SCREEN_B-SCREEN_T)/2-(52-Main.curtain_step)*4))
                pygame.draw.rect(self.screen,(0x7f,0x7f,0x7f),pygame.Rect(SCREEN_L,(SCREEN_B-SCREEN_T)/2+SCREEN_T+(52-Main.curtain_step)*4,
                                                                    SCREEN_R-SCREEN_L,(SCREEN_B-SCREEN_T)/2-(52-Main.curtain_step)*4))
                Main.curtain_step-=1
            else:
                pass
        if Main.game_process==2:
            self.text_numdisplay(Main.current_stage,'B',(155+SCREEN_L+84,201+SCREEN_T))
            self.text_stage.display()
        pygame.display.update()
    
    def creat_stage(self):
        self.screen.fill((0x7f,0x7f,0x7f))
        pygame.draw.rect(self.screen,(1,1,1),pygame.Rect(SCREEN_L,SCREEN_T,SCREEN_R-SCREEN_L,SCREEN_B-SCREEN_T))
        self.event_get3()
        self.draw_creat_map()
        if Main.creat_step>0:
            Main.creat_step-=1
            if Main.creat_step>25:
                self.screen.blit(Main.creat_pointer,(Main.creat_pointer_pos[0]*32+SCREEN_L,Main.creat_pointer_pos[1]*32+SCREEN_T))
        else:
            Main.creat_step=50
            
        if Main.creat_pointer_pressbuf['UP']==1:
            if Main.creat_move_step[0]>0:
                Main.creat_move_step[0]-=1
            if Main.creat_move_step[0]==0:
                #Main.creat_pointer_pos[1] = Main.creat_pointer_pos[1]-1 if Main.creat_pointer_pos[1]-1>=0 else 0
                Main.creat_move_timegap-=1
                if Main.creat_move_timegap==0:
                    
                    Main.creat_step=50
                    Main.creat_pointer_pos[1] = Main.creat_pointer_pos[1]-1 if Main.creat_pointer_pos[1]-1>=0 else 0
                    Main.creat_move_timegap=10
                    if Main.creat_pointer_pressbuf['B']==1:# or Main.creat_pointer_pressbuf['A']==1:
                        tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]=Main.creat_pointer_num
        else:
            Main.creat_move_step[0]=25
        
        if Main.creat_pointer_pressbuf['DOWN']==1:
            if Main.creat_move_step[1]>0:
                Main.creat_move_step[1]-=1
            if Main.creat_move_step[1]==0:
                #Main.creat_pointer_pos[1] = Main.creat_pointer_pos[1]-1 if Main.creat_pointer_pos[1]-1>=0 else 0
                Main.creat_move_timegap-=1
                if Main.creat_move_timegap==0:
                    
                    Main.creat_step=50
                    Main.creat_pointer_pos[1] = Main.creat_pointer_pos[1]+1 if Main.creat_pointer_pos[1]+1<=12 else 12
                    Main.creat_move_timegap=10
                    if Main.creat_pointer_pressbuf['B']==1:# or Main.creat_pointer_pressbuf['A']==1:
                        tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]=Main.creat_pointer_num
        else:
            Main.creat_move_step[1]=25
        
        if Main.creat_pointer_pressbuf['LEFT']==1:
            if Main.creat_move_step[2]>0:
                Main.creat_move_step[2]-=1
            if Main.creat_move_step[2]==0:
                #Main.creat_pointer_pos[1] = Main.creat_pointer_pos[1]-1 if Main.creat_pointer_pos[1]-1>=0 else 0
                Main.creat_move_timegap-=1
                if Main.creat_move_timegap==0:
                    
                    Main.creat_step=50
                    Main.creat_pointer_pos[0] = Main.creat_pointer_pos[0]-1 if Main.creat_pointer_pos[0]-1>=0 else 0
                    Main.creat_move_timegap=10
                    if Main.creat_pointer_pressbuf['B']==1:# or Main.creat_pointer_pressbuf['A']==1:
                        tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]=Main.creat_pointer_num
        else:
            Main.creat_move_step[2]=25
        
        if Main.creat_pointer_pressbuf['RIGHT']==1:
            if Main.creat_move_step[3]>0:
                Main.creat_move_step[3]-=1
            if Main.creat_move_step[3]==0:
                #Main.creat_pointer_pos[1] = Main.creat_pointer_pos[1]-1 if Main.creat_pointer_pos[1]-1>=0 else 0
                Main.creat_move_timegap-=1
                if Main.creat_move_timegap==0:
                    
                    Main.creat_step=50
                    Main.creat_pointer_pos[0] = Main.creat_pointer_pos[0]+1 if Main.creat_pointer_pos[0]+1<=12 else 12
                    Main.creat_move_timegap=10
                    if Main.creat_pointer_pressbuf['B']==1:# or Main.creat_pointer_pressbuf['A']==1:
                        tankmap_mapping[Main.creat_pointer_pos[1]][Main.creat_pointer_pos[0]]=Main.creat_pointer_num
        else:
            Main.creat_move_step[3]=25
        
        
        self.text_numdisplay(Main.creat_stage_num,'B',(SCREEN_L,SCREEN_T-14))
          
        pygame.display.update()
    
    def draw_creat_map(self):
        for i in range(13):
            for j in range(13):
                if (i,j) in homewall_pos:
                    if tankmap_quick_creat[tankmap_mapping[i][j]]==0:
                        if (i,j)==homewall_pos[0]:#homewall_pos=[(11,5),(11,6),(11,7),(12,5),(12,7)]
                            tankmap_creat[i][j]=8
                        elif (i,j)==homewall_pos[1]:
                            tankmap_creat[i][j]=12
                        elif (i,j)==homewall_pos[2]:
                            tankmap_creat[i][j]=4
                        elif (i,j)==homewall_pos[3]:
                            tankmap_creat[i][j]=10
                        elif (i,j)==homewall_pos[4]:
                            tankmap_creat[i][j]=5
                else:
                    tankmap_creat[i][j]=tankmap_quick_creat[tankmap_mapping[i][j]]
                if barrier_pool[tankmap_quick_creat[tankmap_mapping[i][j]]] == 'wall': #1-15
                    c0=tankmap_quick_creat[tankmap_mapping[i][j]]>>3
                    c1=(tankmap_quick_creat[tankmap_mapping[i][j]]>>2)&1
                    c2=(tankmap_quick_creat[tankmap_mapping[i][j]]>>1)&1
                    c3=tankmap_quick_creat[tankmap_mapping[i][j]]&1
                    if c0:
                        self.screen.blit(Main.creat_brick,(SCREEN_T+j*32+16,SCREEN_L+i*32+16))
                    if c1:
                        self.screen.blit(Main.creat_brick,(SCREEN_T+j*32,SCREEN_L+i*32+16))
                    if c2:
                        self.screen.blit(Main.creat_brick,(SCREEN_T+j*32+16,SCREEN_L+i*32))
                    if c3:
                        self.screen.blit(Main.creat_brick,(SCREEN_T+j*32,SCREEN_L+i*32))
                if barrier_pool[tankmap_quick_creat[tankmap_mapping[i][j]]] == 'iron': #16-30
                    c0=(tankmap_quick_creat[tankmap_mapping[i][j]]-15)>>3
                    c1=((tankmap_quick_creat[tankmap_mapping[i][j]]-15)>>2)&1
                    c2=((tankmap_quick_creat[tankmap_mapping[i][j]]-15)>>1)&1
                    c3=(tankmap_quick_creat[tankmap_mapping[i][j]]-15)&1
                    if c0:
                        self.screen.blit(Main.creat_iron,(SCREEN_T+j*32+16,SCREEN_L+i*32+16))
                    if c1:
                        self.screen.blit(Main.creat_iron,(SCREEN_T+j*32,SCREEN_L+i*32+16))
                    if c2:
                        self.screen.blit(Main.creat_iron,(SCREEN_T+j*32+16,SCREEN_L+i*32))
                    if c3:
                        self.screen.blit(Main.creat_iron,(SCREEN_T+j*32,SCREEN_L+i*32))
                if barrier_pool[tankmap_quick_creat[tankmap_mapping[i][j]]] == 'water':#17
                    self.screen.blit(Main.creat_water,(SCREEN_T+j*32,SCREEN_L+i*32))
                if barrier_pool[tankmap_quick_creat[tankmap_mapping[i][j]]] == 'grass':#18
                    self.screen.blit(Main.creat_grass,(SCREEN_T+j*32,SCREEN_L+i*32))
                if barrier_pool[tankmap_quick_creat[tankmap_mapping[i][j]]] == 'ice':#19
                    self.screen.blit(Main.creat_ice,(SCREEN_T+j*32,SCREEN_L+i*32))
        self.screen.blit(Main.creat_eagle,(SCREEN_L+6*32,SCREEN_T+12*32))
    
    #主游戏方法
    def game_run(self):
        
        pygame.init()
        self.remove_all()
        self.screen=pygame.display.set_mode((SCREEN_X,SCREEN_Y))
        pygame.display.set_caption('贱鱼の坦克大战')
        self.text_init()
        while True:
            if Main.process==1:  #1为菜单
                self.event_get1()
                self.menu_display()
                if Main.game_start==True:
                    Main.game_start=False
                    if Main.pointer_pos[1]==1:
                        Main.playernum=1
                        Main.process=2
                        Main.game_process=2
                        self.set_all()
                    elif Main.pointer_pos[1]==2:
                        Main.playernum=2
                        Main.process=2
                        Main.game_process=2
                        self.set_all()
                    elif Main.pointer_pos[1]==3:
                        Main.process=3
                    
            elif Main.process==2:  #2为游戏运行
                self.event_get2()
                if Main.game_process==3:
                    self.object_display()
                self.curtain()
                if Main.enemytankcount==0:
                    if Main.kill_all_step>0:
                        Main.kill_all_step-=1
                    else:
                        Main.kill_all_step=200
                        Main.process=4
            elif Main.process==3:  #3为创作关卡
                self.creat_stage()
            
            elif Main.process==4:  #4为结算关卡
                self.score_display()
            Main.time1.tick(80)
            
#结算关，计算得分
#换关，读取地图
#按键多态化，可移植化
#手柄适配
#鼠标操作
#砖块细化
#

if __name__ == '__main__':
    game=Main()
    game.game_run()
