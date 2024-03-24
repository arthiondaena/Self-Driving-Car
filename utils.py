import pygame
import math

def scale_image(img, factor):
  size = round(img.get_width() * factor), round(img.get_height() * factor)
  return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
  rotated_image = pygame.transform.rotate(image, angle)
  new_rect = rotated_image.get_rect(
    center=image.get_rect(topleft=top_left).center)
  win.blit(rotated_image, new_rect.topleft)

def draw_beam(surface, angle, pos, filpped_masks, render=False):
  c = math.cos(math.radians(angle))
  s = math.sin(math.radians(angle))

  flip_x = c < 0
  flip_y = s < 0
  filpped_mask = filpped_masks[flip_x][flip_y]

  # compute beam final point
  x_dest = surface.get_width() * abs(c)
  y_dest = surface.get_height() * abs(s)

  beam_surface = pygame.Surface(surface.get_rect().center, pygame.SRCALPHA)

  beam_surface.fill((0, 0, 0, 0))

  # draw a single beam to the beam surface based on computed final point
  pygame.draw.line(beam_surface, (0, 0, 255), (0, 0), (x_dest, y_dest))
  beam_mask = pygame.mask.from_surface(beam_surface)

  # find overlap between "global mask" and current beam mask
  offset_x = surface.get_width() - 1 - pos[0] if flip_x else pos[0]
  offset_y = surface.get_height() - 1 - pos[1] if flip_y else pos[1]
  hit = filpped_mask.overlap(beam_mask, (offset_x, offset_y))
  if hit is not None and (hit[0] != pos[0] or hit[1] != pos[1]):
    hx = surface.get_width() - 1 - hit[0] if flip_x else hit[0]
    hy = surface.get_height() - 1 - hit[1] if flip_y else hit[1]
    hit_pos = (hx, hy)
    # visualize rays
    if render:
      line1 = pygame.draw.line(surface, (0, 0, 255), pos, hit_pos)
      pygame.draw.circle(surface, (0, 255, 0), hit_pos, 3)
    return round(math.hypot(hx-pos[0], hy-pos[1]), 2)
  return surface.get_width()
  
def blit_text_center(win, font, text):
  render = font.render(text, 1, (0, 0, 0))
  win.blit(render, (win.get_width()/2 - render.get_width() /
                    2, win.get_height()/2 - render.get_height()/2))
