import pygame


class Button(pygame.sprite.Sprite):
    """
    Esta clase representa los atributos y metodos de un boton
    """

    def __init__(self, x, y, image, weight, height):
        """
        Constructor de la clase Button que inicializa los atributos:
        normalImage, hoverImage, image, rect.x, rect.y
        Parametros:
            x(int): posición inicial en x
            y(int): posición inicial en y
            image(str): dirección archivo de la imagen
            weight(int): Ancho del boton
            height(int): Altura del boton
        """
        pygame.sprite.Sprite.__init__(self)
        sheet = pygame.image.load(image)
        self.normalImage = sheet.subsurface((0, 0, weight, height))
        self.hoverImage = sheet.subsurface((0, height, weight, height))
        self.image = self.normalImage
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def is_clicked(self, pos) -> bool:
        """
        Comprueba si la posición dada está dentro del botón.
        """
        return self.rect.collidepoint(pos)

    def itsNormal(self):
        """
        Este metodo establece como imagen la normalImage
        """
        self.image = self.normalImage

    def itsHover(self):
        """
        Este metodo establece como imagen la hoverImage
        """
        self.image = self.hoverImage
