import pygame


class Body(pygame.sprite.Sprite):
    """Esta es una clase que representa una parte del cuerpo del snake"""

    # Constructor
    def __init__(self, x: int, y: int, image: str):
        """
        Constructor de la clase Body que inicializa los atributos:
        image, rect, rect.x, rect.y, speedx, speedy
        Parametros:
            x(int): posición inicial en x
            y(int): posición inicial en y
            image(str): dirección archivo de la imagen
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = 0
        self.speedy = 0

    def move(self):
        """
        Este metodo actualiza las posiciones X y Y del Body
        """
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def setSpeed(self, speedx, speedy):
        """
        Este metodo actualiza las velocidades en X y Y
        """
        self.speedx = speedx
        self.speedy = speedy

    def getSpeed(self) -> list:
        """
        Este metodo retorna las velocidades del Body
        Return:
            list: Velocidades del Body
        """
        return [self.speedx, self.speedy]

    def setImage(self, image):
        """
        Este metodo actualiza la imagen del objeto
        """
        self.image = pygame.image.load(image).convert()
