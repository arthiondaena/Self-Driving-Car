import pygame
import time
import math
from utils import *
import numpy as np
from goal_maker import make_goals, get_goals
import random

pygame.init()
pygame.font.init()

MAIN_FONT = pygame.font.SysFont("comicsans",44)
SUB_FONT = pygame.font.SysFont("dejavusans",18)
SUB_FONT.italic = True

class GameInfo:
  LAPS = 3
  FPS = 60
  GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.3)
  TRACK = scale_image(pygame.image.load("imgs/track1.png"), 0.5)
  TRACK_BORDER = scale_image(pygame.image.load("imgs/track1_border.png"), 0.5)
  MASK_SURFACE = scale_image(pygame.image.load("imgs/track1_border.png"), 0.5)
  TRACK_BORDER_MASK = pygame.mask.from_surface(MASK_SURFACE)
  FINISH = pygame.image.load("imgs/finish.png")
  FINISH = pygame.transform.rotate(FINISH, 90)
  FINISH_MASK = pygame.mask.from_surface(FINISH)
  FINISH_POSITION = (280, 650)
  WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
  WIN = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption("Racing Game!")

  def __init__(self, players=1):
    self.started = False
    self.lap = 0
    self.race_time = 0
    self.passed_half_lap = False
    self.GOALS = get_goals()
    self.goal_no = 0
    self.finished = False
    self.finish_time = 0
    self.goals_passed = np.full(len(self.GOALS), False)
    self.goals_passed.fill(False)
    self.images = [(self.GRASS, (0, 0)), (self.TRACK, (0,0)),
          (self.FINISH, self.FINISH_POSITION)]
    self.clock = pygame.time.Clock()
    self.computer_car = ComputerCar(8, 10)
    self.rewards = 0
    self.players = players
    if self.players == 2:
      self.player_car = PlayerCar(8, 10)

  def car_passed(self):
    for i in range(len(self.GOALS)):
      # use below line for displaying goals
      # line = pygame.draw.line(self.WIN, (0, 0, 255), self.GOALS[i][0], self.GOALS[i][1])
      rect = pygame.Rect([self.computer_car.x, self.computer_car.y, self.computer_car.CAR_SIZE[0], self.computer_car.CAR_SIZE[1]])

      # if car collides with any of the goal, and goal_passed[i] is False, then increase rewards by 10
      if rect.clipline(self.GOALS[i][0], self.GOALS[i][1]):
        if self.goals_passed[i]==False:
          self.rewards += 10
        self.goals_passed[i] = True
        if i == len(self.GOALS)//2:
          self.passed_half_lap = True

  def next_lap(self):
    # if passed half lap, reset all the goals to False
    if self.passed_half_lap:
      self.goals_passed.fill(False)
  
  def reset(self):
    self.lap = 0
    self.goal_no = 0
    self.computer_car = ComputerCar(8, 10)
    if self.players == 2:
      self.player_car = PlayerCar(8, 10)
    self.goals_passed.fill(False)
    self.rewards = 0
    self.finished = False
    self.race_time = time.time()
    
  def start_lap(self):
    self.reset()
    self.race_time = time.time()
    self.started = True

  def get_time(self):
    if not self.started:
      return 0
    return round(time.time() - self.race_time, 2)

  def track_collision(self, car):
    if car.collide(self.TRACK_BORDER_MASK):
      car.bounce()
      return True

  def gates_passed(self):
    return self.goals_passed.sum()+(self.lap*self.goals_passed.shape[0])

  def draw(self):
    for img, pos, in self.images:
      self.WIN.blit(img, pos)

    if self.players == 2:
      lap_text = MAIN_FONT.render(
          f"Lap {self.player_car.laps}", 1, (255, 255, 255))
    else:
      lap_text = MAIN_FONT.render(
          f"Lap {self.computer_car.laps}", 1, (255, 255, 255))
    self.WIN.blit(lap_text, (10, self.HEIGHT - lap_text.get_height() - 60))

    time_text = MAIN_FONT.render(
      f"Time: {self.get_time()}s", 1, (255, 255, 255))
    self.WIN.blit(time_text, (10, self.HEIGHT - time_text.get_height() - 30))
    
    self.computer_car.draw(self.WIN)
    comptext = SUB_FONT.render("AI", 1, (255, 0, 0))
    self.WIN.blit(comptext, (self.computer_car.x-20, self.computer_car.y-20))

    if self.players == 2:
      self.player_car.draw(self.WIN)
      playertext = SUB_FONT.render("You", 1, (0, 255, 0))
      self.WIN.blit(playertext, (self.player_car.x-20, self.player_car.y-20))

    pygame.display.update()
  
  def draw_actions(self, action):
    pygame.draw.rect(self.WIN,(255,255,255),(800, 100, 40, 40),2)
    pygame.draw.rect(self.WIN,(255,255,255),(850, 100, 40, 40),2)
    pygame.draw.rect(self.WIN,(255,255,255),(900, 100, 40, 40),2)
    pygame.draw.rect(self.WIN,(255,255,255),(850, 50, 40, 40),2)
    pygame.draw.rect(self.WIN, (0, 255, 0), (850, 50, 40, 40))
    
    if action == 0:
      pygame.draw.rect(self.WIN, (0, 255, 0), (850, 100, 40, 40))
    elif action == 1:
      pygame.draw.rect(self.WIN, (0, 255, 0), (800, 100, 40, 40))
    elif action == 2:
      pygame.draw.rect(self.WIN, (0, 255, 0), (900, 100, 40, 40))

    pygame.display.update()

  def check_nextlap(self, car):
    finish_poi_collide = car.finish_collide(self.FINISH_MASK, *self.FINISH_POSITION)

    if finish_poi_collide != None:
      car.next_lap()

  def play_game(self):
    self.clock.tick(self.FPS)
    self.draw()

    if self.players == 2:
      self.player_car.move_player()
      self.track_collision(self.player_car)
      self.player_car.check_half_lap()
      self.check_nextlap(self.player_car)
      if self.player_car.laps == self.LAPS:
        blit_text_center(self.WIN, MAIN_FONT, "You won the game")
        pygame.display.update()
        pygame.time.wait(5000)
        self.reset()
    
    if self.computer_car.laps == self.LAPS:
      blit_text_center(self.WIN, MAIN_FONT, "AI completed race in "+str(self.get_time())+" sec")
      pygame.display.update()
      pygame.time.wait(5000)
      self.reset()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit(0)

    if not self.started:
      self.started = True
      self.start_lap()
    
    pygame.display.update()

  def calculate_rays(self, car, render=False):
    rays = np.zeros(8)

    for angle in range(180, 361, 30):
      rays[(angle-180)//30]=(draw_beam(self.WIN, self.MASK_SURFACE, angle-car.angle, (car.x+10, car.y+20), render=False))

    return rays

  def step(self, action, render=False):
    if not self.started:
      pygame.time.wait(5000)
      self.started = True
      self.start_lap()
    done = False
    old_rewards = self.rewards
    self.computer_car.move_player(action)
    new_state = self.calculate_rays(self.computer_car)
    self.car_passed()
    self.computer_car.check_half_lap()
    self.check_nextlap(self.computer_car)

    if self.computer_car.collide(self.TRACK_BORDER_MASK):
      self.computer_car.vel = -self.computer_car.vel
      done = True
      self.rewards -= 25
    
    if render and self.players == 1:
      self.draw_actions(action)
    
    rewards = self.rewards - old_rewards
    # Small rewards based on current car velocity
    rewards += round(self.computer_car.vel/self.computer_car.max_vel, 2)

    new_state[7] = round(self.computer_car.vel)
    
    return new_state, rewards, done
  

class AbstractCar:
  
  def __init__(self, max_vel, rotation_vel):
    self.img = self.IMG
    self.max_vel = max_vel
    self.vel = 0
    self.rotation_vel = rotation_vel
    self.angle = 270
    self.x, self.y = self.START_POS
    self.acceleration = 0.1
    self.half_lap = ((190, 152), (203, 275))
    self.laps = 0
    self.passed_half_lap = False
  
  def rotate(self, left=False, right=False):
    if left:
      self.angle += self.rotation_vel
    elif right:
      self.angle -= self.rotation_vel
    self.angle %= 360

  def draw(self, win):
    blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
  
  def move_forward(self):
    self.vel = min(self.vel + self.acceleration, self.max_vel)
    self.move()
  
  def move_backward(self, factor=0.5):
    self.vel = max(self.vel - self.acceleration*factor, -self.max_vel)
    self.move()
  
  def move(self):
    radians = math.radians(self.angle)
    vertical = math.cos(radians) * self.vel
    horizontal = math.sin(radians) * self.vel

    self.y -= vertical
    self.x -= horizontal
  
  def reduce_speed(self):
    if self.vel >= 0: 
      self.vel = max(self.vel - self.acceleration/1.5, 0)
    else: 
      self.vel = min(self.vel + self.acceleration/1.5, 0)
    self.move()
  
  def collide(self, mask,x=0, y=0):
    p = (self.x+10, self.y+20)
    car_mask = pygame.mask.Mask(size=(mask.get_size()))
    car_mask.set_at(p, 1)
    poi = mask.overlap(car_mask, (0, 0))
    return poi 
  
  def finish_collide(self, mask, x=0, y=0):
    car_mask = pygame.mask.from_surface(self.img)
    offset = (int(self.x - x), int(self.y - y))
    poi = mask.overlap(car_mask, offset)
    return poi

  def bounce(self):
    self.vel = -self.vel
    self.move()

  def reset(self):
    self.x, self.y = self.START_POS
    self.angle = 0
    self.vel = 0
  
  def check_half_lap(self):
    rect = pygame.Rect([self.x, self.y, self.CAR_SIZE[0], self.CAR_SIZE[1]])
    if rect.clipline(self.half_lap[0], self.half_lap[1]):
      self.passed_half_lap = True
  
  def next_lap(self):
    if self.passed_half_lap:
      self.laps += 1
      self.passed_half_lap = False
    

class ComputerCar(AbstractCar):
  RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
  GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)
  IMG = RED_CAR
  START_POS = (230, 690)
  CAR_SIZE = IMG.get_size()

  def move_player(self, choice):
    # auto acceleration
    self.move_forward()

    if choice == 0:
      self.move_backward()
    elif choice == 1:
      self.rotate(left=True)
    elif choice == 2:
      self.rotate(right=True)
    # do nothing
    elif choice == 3:
      pass
      
    # extra choices which are not used in the model
    elif choice == 4:
      self.move_backward()
    elif choice == 5:
      self.move_forward()
      self.rotate(left=True)
    elif choice == 6:
      self.move_forward()
      self.rotate(right=True)
    elif choice == 7:
      self.move_backward()
      self.rotate(left=True)
    elif choice == 8:
      self.move_backward()
      self.rotate(right=True)
    # friction
    self.reduce_speed()

class PlayerCar(AbstractCar):
  RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
  GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)
  IMG = GREEN_CAR
  START_POS = (230, 650)
  CAR_SIZE = IMG.get_size()

  def move_player(self):
    keys = pygame.key.get_pressed()
    # auto acceleration
    if not keys[pygame.K_s]:
      self.move_forward()
    if keys[pygame.K_a]:
      self.rotate(left=True)
    if keys[pygame.K_d]:
      self.rotate(right=True)
    if keys[pygame.K_s]:
      self.move_backward(2)

    # friction
    self.reduce_speed()