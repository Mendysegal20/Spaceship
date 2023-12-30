import pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 1000,640
path_ship = 'C:/Users/mendy/OneDrive/שולחן העבודה/asteroid_shooter_files/project_3 - Placing elements/graphics/ship.png'


class Ship(pygame.sprite.Sprite):

    # constructor
    def __init__(self,groups):
        # we must initialize the parent class
        super().__init__(groups)

        # we create the surface of the ship
        self.image = pygame.image.load(path_ship).convert_alpha()

        # we create the rect of the ship
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2))

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
            self.can_shoot = False  # we cannot shoot until the laser timer func allows us
            self.shoot_time = pygame.time.get_ticks() # set the shoot time to the current time

    # This method is a timer of the laser that allows us to shoot only after some time
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 500: # if since the last shoot until now more then 5ms have passed
                self.can_shoot = True # we can shoot again

    # This method oporates all the methods and we us it inside the infinite loop game
    def update(self):
        self.laser_timer()
        self.laser_shoot()
        self.input_position()






