import pygame
import time
import math
from utils import *
from goal_maker import make_goals, get_goals
import random


pygame.font.init()

MAIN_FONT = pygame.font.SysFont("comicsans",44)

class GameInfo:
  LAPS = 2
  FPS = 60
  GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
  TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)
  TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
  MASK_SURFACE = scale_image(pygame.image.load("imgs/track_outline.png"), 0.9)
  TRACK_BORDER_MASK = pygame.mask.from_surface(MASK_SURFACE)
  FINISH = pygame.image.load("imgs/finish.png")
  FINISH_MASK = pygame.mask.from_surface(FINISH)
  FINISH_POSITION = (130, 250)
  WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
  WIN = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption("Racing Game!")

  mask = pygame.mask.from_surface(MASK_SURFACE)
  mask_fx = pygame.mask.from_surface(
      pygame.transform.flip(MASK_SURFACE, True, False))
  mask_fy = pygame.mask.from_surface(
      pygame.transform.flip(MASK_SURFACE, False, True))
  mask_fx_fy = pygame.mask.from_surface(
      pygame.transform.flip(MASK_SURFACE, True, True))
  filpped_masks = [[mask, mask_fy], [mask_fx, mask_fx_fy]]

  def __init__(self):
    self.started = False
    self.lap = 0
    self.race_time = 0
    self.passed_half_lap = False
    self.GOALS = get_goals()
    self.goal_no = 0
    self.finished = False
    self.finish_time = 0
    self.goals_passed = [False]*len(self.GOALS)
    self.images = [(self.GRASS, (0, 0)), (self.TRACK, (-2, -14)),
          (self.FINISH, self.FINISH_POSITION), (self.TRACK_BORDER, (-2,-14))]
    self.clock = pygame.time.Clock()
    self.computer_car = ComputerCar(15, 15)
    # self.player_car = PlayerCar(10, 10)
    self.rewards = 0

  def car_passed(self):
    for i in range(len(self.GOALS)):
      # line = pygame.draw.line(self.WIN, (0, 0, 255), self.GOALS[i][0], self.GOALS[i][1])
      rect = pygame.Rect([self.computer_car.x, self.computer_car.y, self.computer_car.CAR_SIZE[0], self.computer_car.CAR_SIZE[1]])

      if rect.clipline(self.GOALS[i][0], self.GOALS[i][1]):
        if self.goals_passed[i] is False:
          self.rewards += 1
        self.goals_passed[i] = True
        if i == len(self.GOALS)/2:
          self.passed_half_lap = True

  def next_lap(self):
    if self.passed_half_lap:
      self.lap += 1
      self.goals_passed = [False]*len(self.GOALS)
      self.passed_half_lap = False
    if self.lap == self.LAPS:
      self.finished = True
      self.finish_time = self.get_time()
      self.started = False
  
  def reset(self):
    self.lap = 0
    self.goal_no = 0
    self.computer_car = ComputerCar(10, 10)
    # self.player_car = PlayerCar(10, 10)
    self.started = True
  
  def start_lap(self):
    self.reset()
    self.race_time = time.time()
    self.started = True

  def get_time(self):
    if not self.started:
      return 0
    return round(time.time() - self.race_time, 2)

  def track_collision(self, car):
    if car.collide(self.TRACK_BORDER_MASK) != None:
      car.bounce()
      return True


  def draw(self):
    for img, pos, in self.images:
      self.WIN.blit(img, pos)

    lap_text = MAIN_FONT.render(
        f"Lap {game_info.lap}", 1, (255, 255, 255))
    self.WIN.blit(lap_text, (10, self.HEIGHT - lap_text.get_height() - 60))

    time_text = MAIN_FONT.render(
      f"Time: {game_info.get_time()}s", 1, (255, 255, 255))
    self.WIN.blit(time_text, (10, self.HEIGHT - time_text.get_height() - 30))
    
    # self.player_car.draw(self.WIN)
    self.computer_car.draw(self.WIN)
    pygame.display.update()

  def play_game(self, render=False):
    run = True
    while run:
      self.clock.tick(self.FPS)

      if render:
        self.draw()
        # while not self.started:
        #   if not self.finished:
        #     blit_text_center(self.WIN, MAIN_FONT, f"Press any key.")
        #   else:
        #     blit_text_center(self.WIN, MAIN_FONT, f"Time: {self.finish_time}.")
        #   pygame.display.update()

        #   for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #       pygame.quit()
        #       break
            
        #     if event.type == pygame.KEYDOWN:
        #       self.start_lap()
      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          break
        
        if event.type == pygame.KEYDOWN and not self.started:
          self.start_lap()

      # self.player_car.move_player()
      # self.track_collision(self.player_car)
      self.track_collision(self.computer_car)
      self.car_passed()
      # self.step(random.randint(0, 9))

      finish_poi_collide = self.computer_car.collide(self.FINISH_MASK, *self.FINISH_POSITION)

      if finish_poi_collide != None:
        self.next_lap()
      
      # self.calculate_rays(self.player_car)
      self.calculate_rays(self.computer_car)

      # print(self.rewards)
      
      pygame.display.update()
      # break

  def calculate_rays(self, car):
    rays = []
    for angle in range(180, 361, 30):
      rays.append(draw_beam(self.WIN, angle-car.angle, (car.x+10, car.y+20), self.filpped_masks))
    for i in range(len(rays)):
      rays[i] = ((1000 - rays[i]) / 1000)
    return rays

  def step(self, action):
    if action == 0 and not self.started:
      self.started = True
      self.start_lap = True
    done = False
    old_rewards = self.rewards
    self.computer_car.move_player(action)
    new_state = self.calculate_rays(self.computer_car)
    # print('action', action)

    if self.track_collision(self.computer_car):
      done = True
      self.rewards -= 1
    
    rewards = self.rewards - old_rewards
    
    if done:
      new_state = None
    
    return new_state, rewards, done
    

class AbstractCar:
  
  def __init__(self, max_vel, rotation_vel):
    self.img = self.IMG
    self.max_vel = max_vel
    self.vel = 0
    self.rotation_vel = rotation_vel
    self.angle = 0
    self.x, self.y = self.START_POS
    self.acceleration = 0.1
  
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
  
  def move_backward(self):
    self.vel = max(self.vel - self.acceleration, -self.max_vel)
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
  
  def collide(self, mask, x=0, y=0):
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

class ComputerCar(AbstractCar):
  RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
  GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)
  IMG = RED_CAR
  START_POS = (180, 200)
  CAR_SIZE = IMG.get_size()

  def move_player(self, choice):
    moved = False

    if choice == 0:
      pass
    elif choice == 1:
      moved = True
      self.move_forward()
    elif choice == 2:
      self.rotate(left=True)
    elif choice == 3:
      self.rotate(right=True)
    elif choice == 4:
      moved = True
      self.move_backward()
    elif choice == 5:
      moved = True
      self.move_forward()
      self.rotate(left=True)
    elif choice == 6:
      moved = True
      self.move_forward()
      self.rotate(right=True)
    elif choice == 7:
      moved = True
      self.move_backward()
      self.rotate(left=True)
    elif choice == 8:
      moved = True
      self.move_backward()
      self.rotate(right=True)

class PlayerCar(AbstractCar):
  RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
  GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)
  IMG = GREEN_CAR
  START_POS = (160, 200)
  CAR_SIZE = IMG.get_size()

  def move_player(self):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
      self.rotate(left=True)
    if keys[pygame.K_d]:
      self.rotate(right=True)
    if keys[pygame.K_w]:
      moved = True
      self.move_forward()
    if keys[pygame.K_s]:
      moved = True
      self.move_backward()

    if not moved:
      self.reduce_speed()


game_info = GameInfo()

# game_info.play_game(True)
  
# pygame.quit()