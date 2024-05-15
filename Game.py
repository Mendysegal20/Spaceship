import pygame
from settings import *
from sys import exit
from random import randint,uniform


class Ship(pygame.sprite.Sprite):

    # constructor
    def __init__(self, groups):
        # we must initialize the parent class
        super().__init__(groups)

        # we create the surface of the ship
        self.image = pygame.image.load(path_ship).convert_alpha()

        # we create the rect of the ship
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # add a mask for butter looking collisions
        self.mask = pygame.mask.from_surface(self.image)

        # the laser's sound
        self.laser_sound = pygame.mixer.Sound(laser_sound_path)

        # flags that indicates if we can shoot and when we shoot
        self.can_shoot = True
        self.shoot_time = None

    # This method places the ship in the location of the mouse
    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    # This method takes care of the shoot and determans if we can shoot
    def laser_shoot(self):
        # if we pressed the mouse and we can shoot
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            Laser(self.rect.midtop,laser_group)
            self.laser_sound.play()
            self.can_shoot = False  # we cannot shoot until the laser timer func allows us
            self.shoot_time = pygame.time.get_ticks()  # set the shoot time to the current time

    # This method is a timer of the laser that allows us to shoot only after some time
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 200:  # if since the last shoot until now more then 5ms have passed
                self.can_shoot = True  # we can shoot again

    # collisions
    def meteor_collision(self):
        use_mask = pygame.sprite.collide_mask # we use the mask insted of rect for collisions
        collided_meteors = pygame.sprite.spritecollide(self,meteor_group,False,use_mask)
        if len(collided_meteors) > 0:
            pygame.quit()
            exit()

    # This method oporates all the methods and we us it inside the infinite loop game
    def update(self):
        self.laser_timer()
        self.laser_shoot()
        self.input_position()
        self.meteor_collision()


class Laser(pygame.sprite.Sprite):
    def __init__(self,position,groups): # constructor

        # call father constructor
        super().__init__(groups)

        # we create the surface and rect of the laser
        self.image = pygame.image.load(path_laser).convert_alpha()
        self.rect = self.image.get_rect(midbottom=position)

        # add a mask for butter looking collisions
        self.mask = pygame.mask.from_surface(self.image)

        # meteor explosion's sound
        self.explosion_sound = pygame.mixer.Sound(meteor_sound_path)

        # float based positions of rect
        self.pos = pygame.math.Vector2(self.rect.topleft) # position of laser
        self.direction = pygame.math.Vector2((0,-1)) # direction of laser
        self.speed = 600 # speed of laser

    def meteor_collision(self):
        use_mask = pygame.sprite.collide_mask  # we use the mask insted of rect for collisions
        collided_meteors = pygame.sprite.spritecollide(self, meteor_group, True,use_mask)
        if len(collided_meteors) > 0:
            self.explosion_sound.play()
            self.kill()

    def update(self):
        # we change the position of the laser rect
        self.pos += self.direction * self.speed * dt

        # important! we have to actually update the position of the rect
        self.rect.topleft = (round(self.pos.x),round(self.pos.y))

        # check for collisions with meteors
        self.meteor_collision()

        # if the laser did not collide with any meteor we will destroy it ourselves
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self,position,groups):

        # our basic setup
        super().__init__(groups)
        meteor_surf = pygame.image.load(path_meteor).convert_alpha()
        meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5,1.5)
        self.scaled_surf = pygame.transform.scale(meteor_surf, meteor_size)
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(center=position)

        # float based positions of rect
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(400,600)

        # rotation
        self.rotation = 0
        self.rotation_speed = randint(20,50)

        # add a mask for butter looking collisions
        self.mask = pygame.mask.from_surface(self.image)

    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotate_surf = pygame.transform.rotozoom(self.scaled_surf,self.rotation,1)
        self.image = rotate_surf
        self.mask = pygame.mask.from_surface(self.image) # update the mask
        self.rect = self.image.get_rect(center=self.rect.center) # update the rect

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x),round(self.pos.y))
        self.rotate()

        # if the meteor did not collide with any laser we will destroy it ourselves
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


class Score:
    def __init__(self):
        self.font = pygame.font.Font(path_text,50)

    def display(self):
        score_text = f'Score {pygame.time.get_ticks() // 1000}'
        text_surf = self.font.render(score_text, True, 'white')
        text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
        display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(display_surface, 'white', text_rect.inflate(30, 30), width=8, border_radius=5)


# basic setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 640
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space shooter')
clock = pygame.time.Clock()

# background
background_surf = pygame.image.load(path_bg).convert()

# sprite groups
ship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# sprite creation
ship = Ship(ship_group)

# meteor timer
meteor_timer = pygame.event.custom_type()
# pygame will arise this event every half a second. every half a second there will be meteor created
pygame.time.set_timer(meteor_timer,500)


# score
score = Score()

# game sound
game_sound = pygame.mixer.Sound(game_sound_path)
game_sound.play(loops=-1) # we play it in an infinite loop

# game loop
while True:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # if half a second has passed we create another meteor
        if event.type == meteor_timer:
            x_pos = randint(-100,WINDOW_WIDTH + 100)
            y_pos = randint(-150,-50)
            Meteor((x_pos,y_pos),meteor_group)

    # delta time
    dt = clock.tick() / 1000

    # background
    display_surface.blit(background_surf, (0, 0))

    # update
    ship_group.update()
    laser_group.update()
    meteor_group.update()

    # score
    score.display()

    # graphics
    ship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)

    # draw the frame
    pygame.display.update()


