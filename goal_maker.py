import pygame

def get_goals():
  goals = [((227, 192),(118, 194)),((225, 156),(117, 156)),((226, 89),(117, 132)),
            ((178, 24),(120, 125)),((49, 31),(113, 127)),((3, 157),(112, 151)),
            ((4, 206),(119, 212)),((4, 287),(112, 284)),
            ((225, 170), (117, 167)), ((203, 57), (122, 114)), ((31, 56), (109, 112)), 
            ((12, 234), (105, 233)), ((12, 333), (107, 336)), ((15, 435), (102, 426)), 
            ((48, 514), (124, 472)), ((115, 588), (190, 533)), ((176, 656), (257, 603)), 
            ((265, 743), (324, 661)), ((407, 748), (359, 659)), ((457, 619), (362, 615)), 
            ((468, 519), (399, 452)), ((535, 530), (596, 439)), ((544, 644), (644, 634)), 
            ((644, 634), (672, 675)), ((672, 771), (672, 771)), ((695, 640), (694, 639)), 
            ((694, 639), (795, 646)), ((687, 518), (794, 512)), ((684, 419), (792, 405)), 
            ((637, 398), (629, 299)), ((531, 405), (524, 300)), ((445, 298), (352, 299)), 
            ((540, 299), (542, 196)), ((692, 298), (668, 194)), ((684, 153), (792, 157)), 
            ((664, 117), (656, 10)), ((656, 11), (539, 116)), ((528, 10), (386, 117)), 
            ((377, 13), (332, 121)), ((332, 121), (225, 128)), ((335, 208), (226, 213)), 
            ((226, 213), (228, 213)), ((228, 213), (336, 258)), ((226, 270), (321, 394)), 
            ((234, 354), (144, 402)), ((215, 348), (128, 266))]
  return goals

GOALS = []
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


# ans = []
# for i in range(0, len(goals), 2):
#   ans.append((goals[i], goals[i+1]))

# print(ans)