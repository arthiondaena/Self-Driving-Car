import pygame
import time
import math
from utils import *
from goal_maker import make_goals, get_goals


pygame.font.init()
GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)

TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)

mask_surface = scale_image(pygame.image.load("imgs/track_outline.png"), 0.9)
mask_pos = (2,14)

# TRACK_BORDER = mask_surface

TRACK_BORDER_MASK = pygame.mask.from_surface(mask_surface)
FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

MAIN_FONT = pygame.font.SysFont("comicsans",44)

FPS = 60

class GameInfo:
  LAPS = 2
  FPS = 60
  
  GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
  TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)
  TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
  MASK_SURFACE = scale_image(pygame.image.load("imgs/track_outline.png"), 0.9)
  mask_pos = (2,14)
  TRACK_BORDER_MASK = pygame.mask.from_surface(mask_surface)
  FINISH = pygame.image.load("imgs/finish.png")
  FINISH_MASK = pygame.mask.from_surface(FINISH)
  FINISH_POSITION = (130, 250)

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

  def car_passed(self, player_car, WIN):
    for i in range(len(self.GOALS)):
      # line = pygame.draw.line(WIN, (0, 0, 255), self.GOALS[i][0], self.GOALS[i][1])
      rect = pygame.Rect([player_car.x, player_car.y, player_car.CAR_SIZE[0], player_car.CAR_SIZE[1]])

      if rect.clipline(self.GOALS[i][0], self.GOALS[i][1]):
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
  
  def start_lap(self):
    self.reset()
    self.race_time = time.time()
    self.started = True

  def get_time(self):
    if not self.started:
      return 0
    return round(time.time() - self.race_time, 2)


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


def draw(win, images, computer_car, game_info):
  for img, pos, in images:
    win.blit(img, pos)

  lap_text = MAIN_FONT.render(
      f"Lap {game_info.lap}", 1, (255, 255, 255))
  win.blit(lap_text, (10, HEIGHT - lap_text.get_height() - 60))

  time_text = MAIN_FONT.render(
    f"Time: {game_info.get_time()}s", 1, (255, 255, 255))
  win.blit(time_text, (10, HEIGHT - time_text.get_height() - 30))
  
  player_car.draw(win)
  pygame.display.update()


clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (-2, -14)),
          (FINISH, FINISH_POSITION), (TRACK_BORDER, (-2,-14))]
player_car = PlayerCar(8, 8)

mask = pygame.mask.from_surface(mask_surface)
mask_fx = pygame.mask.from_surface(
    pygame.transform.flip(mask_surface, True, False))
mask_fy = pygame.mask.from_surface(
    pygame.transform.flip(mask_surface, False, True))
mask_fx_fy = pygame.mask.from_surface(
    pygame.transform.flip(mask_surface, True, True))
filpped_masks = [[mask, mask_fy], [mask_fx, mask_fx_fy]]

game_info = GameInfo()

def play_game():
  run = True
  while run:
    clock.tick(FPS)

    draw(WIN, images, player_car, game_info)

    while not game_info.started:
      if not game_info.finished:
        blit_text_center(WIN, MAIN_FONT, f"Press any key.")
      else:
        blit_text_center(WIN, MAIN_FONT, f"Time: {game_info.finish_time}.")
      pygame.display.update()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          break
        
        if event.type == pygame.KEYDOWN:
          game_info.start_lap()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        break
      if pygame.mouse.get_pressed()[0]: # if left button of the mouse pressed
        print(pygame.mouse.get_pos())
      
    player_car.move_player()

    if player_car.collide(TRACK_BORDER_MASK) != None:
      player_car.bounce()
    
    game_info.car_passed(player_car, WIN)

    finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)

    if finish_poi_collide != None:
      game_info.next_lap()
    
    lines = []
    for angle in range(180, 361, 30):
      lines.append(draw_beam(WIN, angle-player_car.angle, (player_car.x+10, player_car.y+20), filpped_masks))
    print(lines)
    
    pygame.display.update()
  
  pygame.quit()