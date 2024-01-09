
from images import *

bones = pygame.sprite.Group()
bgs = pygame.sprite.Group()
all_bone_list = []


class Bone(pygame.sprite.Sprite):
    def __init__(self, nominal: tuple):
        pygame.sprite.Sprite.__init__(self)
        self.image = eval(f'bone_{nominal[0]}_{nominal[1]}_image')
        self.back_image = bone_back_image
        self.rect = self.image.get_rect()
        self.nominal = nominal
        self.name = str(self.nominal)
        if nominal[0] == nominal[1]:
            self.double = True
        else:
            self.double = False
        self.add(bones)


class Bg(pygame.sprite.Sprite):
    def __init__(self, flag: str):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 100))
        if flag == 't':
            self.image.fill(color='aquamarine4')
        if flag == 'b':
            self.image.fill(color='cyan3')
        self.rect = self.image.get_rect()
        self.add(bgs)


def set_bones():
    for y in range(7):
        all_bone_list.extend([(y, x) for x in range(7) if x >= y])
    for i in all_bone_list:
        Bone(i)


set_bones()
