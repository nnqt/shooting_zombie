import pygame
from pygame.locals import *
from zombie import Zombie
import random
from pointer import pointer


class Game:
  FPS = 30
  DISPLAY_W = 1280
  DISPLAY_H = 720
  flag_screen = pygame.FULLSCREEN
  DEFAULT_BACKGROUND_SIZE = (DISPLAY_W, DISPLAY_H )
  DEFAULT_TUPLE_SIZE = (80, 100 )
  BG_COLOR = (120, 120, 120)
  zombies = []
  noZombie = 0
  posTuple = [(100, 524), (250, 524), (400, 524), (600, 524),
                (850, 524), (1040, 140), (1200, 524)]
  ableTuple = [(100, 524), (250, 524), (400, 524), (600, 524),
                (850, 524), (1040, 140), (1200, 524)]
  unableTuple = []
  zombie_img_path = 'assets/zombie_walking.png'
  bg_img_path = 'assets/background.png'
  tuple_img_path = 'assets/tuple.png'
  button_img_path = 'assets/button.png'
  bullet_sound_path = 'assets/ak47.wav'
  headshot_sound_path = 'assets/headshot.wav'
  music_path = 'assets/music.mp3'


  def __init__(self) -> None:
    self.game = pygame
    pass

  def init(self):
    self.game.init()
    self.font = pygame.font.SysFont('comicsans', 35)
    self.game.mixer.music.load(self.music_path)
    self.game.mixer.music.set_volume(0.2)
    self.game.mixer.music.play()
    self.game.mouse.set_visible(False)
    self.size = (self.DISPLAY_W, self.DISPLAY_H)
    self.window = self.game.display.set_mode(self.size, self.flag_screen)
    self.clock = self.game.time.Clock()
    self.running = False
    self.menu_running = True

    self.score_hit = 0
    self.score_miss = 0
    self.score_count = 0
    self.score_headshot = 0

    self.pointer = pointer()
    self.crosshair = pygame.sprite.Group(self.pointer)

    # background
    self.bg_image = pygame.image.load(self.bg_img_path).convert_alpha()
    self.bg_image = pygame.transform.scale(self.bg_image, self.DEFAULT_BACKGROUND_SIZE)

    # tuple
    self.tuple_image = pygame.image.load(self.tuple_img_path).convert_alpha()
    self.tuple_image = pygame.transform.scale(self.tuple_image, self.DEFAULT_TUPLE_SIZE)

    # start button
    self.button_image = pygame.image.load(self.button_img_path)
    self.button_image = pygame.transform.scale(self.button_image, (500, 500))
    self.start_image_rect = (125, 45, 250, 70)
    # self.button_image = pygame.transform.chop(self.start_button_1, (10, 100, 160, 500))

    # timer for animation hit
    self.list_hit_animation = []

      

    # sound
    self.bullet_sound = pygame.mixer.Sound(self.bullet_sound_path)
    self.headshot_sound = pygame.mixer.Sound(self.headshot_sound_path)
    self.headshot_sound.set_volume(0.12)

    # zombie
    self.zombie_group = pygame.sprite.Group()
    for i in range(4):
      self.addNewZombie()

    

  def run(self):
    while self.running:
      self.clock.tick(self.FPS)
      self.current_time = pygame.time.get_ticks()

      for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
          self.running = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_F11:
            if self.flag_screen == pygame.FULLSCREEN:
              self.flag_screen = pygame.RESIZABLE
            elif self.flag_screen == pygame.RESIZABLE:
              self.flag_screen = pygame.FULLSCREEN
            self.window = self.game.display.set_mode(self.size, self.flag_screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
          
          self.bullet_sound.play()
          flag = False
          for i in range (self.noZombie):
            check_hit = self.hit(self.zombies[i])
            if(check_hit == "headshot"):
              
              self.list_hit_animation.append((pygame.mouse.get_pos(),self.current_time + 500, 100))
              self.score_headshot += 1
              self.score_hit += 1
              flag = True
            elif(check_hit == "hit"):
              self.list_hit_animation.append((pygame.mouse.get_pos(),self.current_time + 500, 50))
              self.score_hit += 1
              flag = True
          if flag == False:
            self.score_miss += 1
          self.score_count += 1


      self.drawBackground()
      self.drawZombie()
      self.drawTuple()
      if(self.list_hit_animation):
        for hit in self.list_hit_animation:
          (x, y) = hit[0]
          timer = hit[1]
          damage = hit[2]
          if self.drawHitAnimation(x, y, timer, damage):
            pass
          else:
            self.list_hit_animation.remove(hit)
      self.drawScore()
      self.drawCrosshair()
      self.update()


  def runMenu(self):
    while self.menu_running:
      self.clock.tick(self.FPS)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.menu_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
          self.menu_running =False
          self.running = True

      self.drawBackground()
      self.drawStart()
      self.drawCrosshair()
      self.game.display.update()

  def drawZombie(self):
    # zombie
    for i in range(self.noZombie):
      if(self.current_time < self.zombies[i].getTimer()):
        self.zombies[i].animation(self.window)
      else:
        self.killZombie(self.zombies[i])

    # self.game.display.update()

  def drawBackground(self):
    # background
    self.window.blit(self.bg_image, (0,0))

  def drawTuple(self):
    # tuple
    for i in range (len(self.posTuple)):
      self.window.blit(self.tuple_image, self.posTuple[i])

  def drawCrosshair(self):
    # crosshair
    self.crosshair.update()
    self.pointer.show(self.window)
    # self.crosshair.draw(self.window)

  def drawScore(self):
    score_hit_text = self.font.render("HIT : " + str(self.score_hit), True, (0,0,0))
    self.window.blit(score_hit_text, (100, 10))

    score_miss_text = self.font.render("MISS : " + str(self.score_miss), True, (0,0,0))
    self.window.blit(score_miss_text, (100, 50))
    
    if self.score_count == 0:
      score_percent = 1.0  
    else:
      score_percent = round((self.score_hit / self.score_count), 4)
    score_percent_text = self.font.render("ACCURACY : " + str(round(score_percent * 100.0, 2)) + "%", True, (0,0,0))
    self.window.blit(score_percent_text, (100, 90))

    score_headshot_text = self.font.render("HEADSHOT : " + str(self.score_headshot), True, (0,0,0))
    self.window.blit(score_headshot_text, (100, 130))

  def drawHitAnimation(self, x, y, timer, damage):
    scoreText = self.font.render("-" + str(damage), True, (0,0,0))
    if self.current_time < timer:
      if(x + 80) > self.DISPLAY_W:
        x -= 100
      self.window.blit(scoreText, (x + 40, y - 40))
      return True
    pygame.display.flip()
    return False

  def drawStart(self):
    # start button
    self.window.blit(self.button_image, (540, 325), self.start_image_rect)

  def update(self):
    for i in range (self.noZombie):
      self.zombies[i].appear()

    self.crosshair.update()
    self.pointer.show(self.window)
    if(self.checkDeathZombie()):
      death = self.checkDeathZombie()
      self.killZombie(death)

    self.game.display.update()

  def checkCollisionZombie(self, zombie):
    offset_x = zombie.getX() - self.pointer.rect.left
    offset_y = zombie.getY() - self.pointer.rect.top
    if self.pointer.mask.overlap(zombie.mask_body, (offset_x , offset_y)):
      return True

    return False

  def checkCollisionZombieHead(self, zombie):
    offset_x = zombie.getX() - self.pointer.rect.left
    offset_y = zombie.getY() - self.pointer.rect.top
    if self.pointer.mask.overlap(zombie.mask_head, (offset_x , offset_y)):
      return True
    return False

  def checkCollisionTuple(self):
    pos = pygame.mouse.get_pos()

    for i in range(len(self.posTuple)):
      if (self.posTuple[i][0] < pos[0] < self.posTuple[i][0] + self.DEFAULT_TUPLE_SIZE[0]) and (self.posTuple[i][1] < pos[1] < self.posTuple[i][1] + self.DEFAULT_TUPLE_SIZE[1]):
        return True
    return False

  def checkCollisionStart(self):
    pass

  def hit(self, zombie):
    if(self.checkCollisionZombieHead(zombie)):
      self.headshot_sound.play()
      zombie.decreaseHeath(100)
      return "headshot"
    elif not self.checkCollisionZombie(zombie):
      return "miss"
    else:
      zombie.decreaseHeath(50)
      return "hit"

  def choiceTuple (self, num):
    return random.sample(self.ableTuple, num)

  def removeTuple (self, tuple):
    temp = tuple[0]
    self.unableTuple.append(temp)
    for x in tuple:
      self.ableTuple.remove(x)

  def addNewZombie (self):
    temp = self.choiceTuple(1)
    self.removeTuple(temp)
    x,y = temp[0]
    timer = pygame.time.get_ticks() + 7000
    obj = Zombie(self.zombie_img_path, 3, x , y , timer)
    self.zombies.append(obj)
    self.zombie_group.add(self.zombies[len(self.zombies) - 1])

    self.noZombie += 1

  def killZombie (self, zombie):
    temp = ()
    for i in range(len(self.posTuple)):
      if zombie.getX() == self.posTuple[i][0]:
        temp = self.posTuple[i]
    self.zombies.remove(zombie)
    self.zombie_group.remove(zombie)
    self.unableTuple.remove(temp)
    self.ableTuple.append(temp)

    self.addNewZombie()

    self.noZombie -= 1

  def checkDeathZombie(self):
    for i in range (self.noZombie):
      if(self.zombies[i].getHeath() <= 0):
        return self.zombies[i]

if __name__ == '__main__':
    g = Game()
    g.init()
    g.runMenu()
    g.run()

