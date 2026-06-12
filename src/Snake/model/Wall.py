import pygame

class Wall(pygame.sprite.Sprite):
    """
        Esta clase representa los atributos de un Muro
    """

    # Constructor
    def __init__(self, x, y, image):
        """
            Constructor de la clase Wall que inicializa los atributos:
            image, rect, rect.x, rect.y
            Parametros: 
                x(int): posición inicial en x
                y(int): posición inicial en y
                image(str): dirección archivo de la imagen
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y