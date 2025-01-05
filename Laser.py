import pygame

path_laser = '../SpaceShip/const/graphics/laser.png'


class Laser(pygame.sprite.Sprite):
    def __init__(self,position,groups): # constructor

        # call father constructor
        super().__init__(groups)

        # we create the surface of the laser
        self.image = pygame.image.load(path_laser).convert_alpha()

        # we create the rect of the laser
        self.rect = self.image.get_rect(midbottom=position)

        # float based position of rect
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self):
        self.pos.y -= 10