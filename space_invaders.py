import pygame, sys
from player import Player
import obstacles
from alien import Alien
from random import choice
from laser import Laser


class Game:
  def __init__(self):
    player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
    self.player = pygame.sprite.GroupSingle(player_sprite)
    
  #obstaculos
    self.shape = obstacles.shape 
    self.block_size = 6
    self.blocks = pygame.sprite.Group()
    self.obstacle_amount = 4
    self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range (self.obstacle_amount)]
    self.create_multiple_obstacles(*self.obstacle_x_positions, x_start= screen_width / 15, y_start=480)
    
  # aliens setup
  
    self.aliens = pygame.sprite.Group()
    self.alien_lasers = pygame.sprite.Group()
    self.alien_setup(rows= 6, cols = 8)
    self.alien_direction = 1
    self.alien_lasers = pygame.sprite.Group()

    
  def create_obstacle(self, x_start, y_start, offset_x):
    for row_index, row in enumerate(self.shape):
      for col_index, col in enumerate(row):
        if col == 'x':
          x = x_start + col_index  * self.block_size + offset_x
          y = y_start + row_index * self.block_size
          block = obstacles.Block(self.block_size,(241,79,80),x,y)
          self.blocks.add(block)
  
  def create_multiple_obstacles(self,*offset,x_start, y_start):
    for offset_x in offset:
      self.create_obstacle(x_start,y_start, offset_x)
  
  def alien_setup(self,rows,cols,x_distance = 60,y_distance = 48, x_offset = 70, y_offset = 100):
    for row_index, row in enumerate(range(rows)):
      for col_index, col in enumerate(range(cols)):
        x =  col_index * x_distance + x_offset
        y =  row_index * y_distance + y_offset
        
        if row_index == 0: alien_sprite = Alien('yellow',x,y)
        elif 1 <= row_index <= 2: alien_sprite = Alien('green',x,y)
        else: alien_sprite = Alien('red',x,y)
        self.aliens.add(alien_sprite)
  
  def alien_position_checker(self):
    all_aliens = self.aliens.sprites()
    for alien in all_aliens:
      if alien.rect.right >= screen_width:
          self.alien_direction = -1
          self.alien_move_down(2)
      elif alien.rect.left <= 0:
          self.alien_direction = 1
          self.alien_move_down(2)
  
  def alien_move_down(self,distance):
    if self.aliens:
      for alien in self.aliens.sprites():
        alien.rect.y += distance
  def alien_shoot(self):
    if self.aliens.sprites():
      random_alien = choice(self.aliens.sprites())
      laser_sprite = Laser(random_alien.rect.center,5,screen_height)
      self.alien_lasers.add(laser_sprite)
      
  def run(self):
    self.player.update()
    self.aliens.update(self.alien_direction)
    
    self.player.sprite.lasers.draw(screen)
    self.alien_position_checker()
    self.alien_shoot()
    self.alien_lasers.update()
    self.player.draw(screen)
    self.aliens.draw(screen)
    self.blocks.draw(screen)
    self.alien_lasers.draw(screen)

    

if __name__ == '__main__':
  pygame.init()
  screen_width = 600
  screen_height = 600
  screen = pygame.display.set_mode((screen_width,screen_height))
  clock = pygame.time.Clock()
  game = Game()

  ALIENLASER = pygame.USEREVENT + 1
  pygame.time.set_timer(ALIENLASER, 800)
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    screen.fill((30,30,30))
    game.run()
    pygame.display.flip()
    clock.tick(60)