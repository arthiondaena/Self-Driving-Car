import pygame

def get_goals():
  goals = [((294, 638),(297, 750)), ((426, 641), (435, 753)), ((575, 639), (579, 754)), ((713, 639), (712, 754)), 
            ((785, 627), (868, 725)), ((803, 586), (918, 583)), ((799, 506), (912, 503)), ((803, 408), (917, 407)), 
            ((803, 335), (915, 339)), ((768, 265), (828, 164)), ((654, 151), (646, 263)), ((495, 67), (498, 189)), 
            ((344, 152), (350, 263)), ((190, 152), (203, 275)), ((71, 308), (194, 300)), ((227, 435), (243, 297)), 
            ((339, 438), (342, 310)), ((420, 430), (422, 308)), ((532, 432), (611, 311)), ((533, 460), (685, 471)), 
            ((474, 461), (469, 602)), ((340, 467), (345, 599)), ((169, 471), (229, 600)), ((63, 611), (205, 604)), 
            ((210, 630), (210, 757))]
  return goals

GOALS = []

# Use this to make goals
def make_goals():
  GOALS = []
  goal = []
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
        print(GOALS)
        break
      if pygame.mouse.get_pressed()[0]: # if left button of the mouse pressed
        goal.append(pygame.mouse.get_pos())
  if len(goal) == 2:
    GOALS.append(goal[0], goal[1])
    print(GOALS)
    goal = []
  return