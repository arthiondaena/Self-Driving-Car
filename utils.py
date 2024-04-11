import pygame
import math
from copy import copy

def scale_image(img, factor):
  size = round(img.get_width() * factor), round(img.get_height() * factor)
  return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
  rotated_image = pygame.transform.rotate(image, angle)
  new_rect = rotated_image.get_rect(
    center=image.get_rect(topleft=top_left).center)
  win.blit(rotated_image, new_rect.topleft)

def draw_beam(surface, mask, angle, pos, render=False):
  c = math.cos(math.radians(angle))
  s = math.sin(math.radians(angle))
  
  step_size = 2
  max_steps = 100
  max_dist = max_steps * step_size

  query_pos = copy(pos)
  ratio = 0
  hit = False

  mask.lock()

  for step in range(max_steps):
      ratio = (step + 1) / max_steps

      query_pos = (pos[0] + c * ratio * max_dist, pos[1] + s * ratio * max_dist)

      if query_pos[0] < 0 or query_pos[0] >= mask.get_width() or query_pos[1] < 0 or query_pos[1] >= mask.get_height():
          break
      # try:
      color = mask.get_at((int(query_pos[0] + 0.5), int(query_pos[1] + 0.5)))
      if color[3] > 127:
          hit = True
          break
      # except:
      #   pass

  mask.unlock()

  if render and hit:
    line1 = pygame.draw.line(surface, (0, 0, 255), pos, query_pos)
    pygame.draw.circle(surface, (0, 255, 0), query_pos, 3)

  return ratio * max_dist
  
def blit_text_center(win, font, text):
  render = font.render(text, 1, (0, 0, 0))
  win.blit(render, (win.get_width()/2 - render.get_width() /
                    2, win.get_height()/2 - render.get_height()/2))
