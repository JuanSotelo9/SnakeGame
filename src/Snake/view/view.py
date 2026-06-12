import pygame


WHITE = (255,255,255)
BLACK = (0,0,0)

class View:
    """
        Esta clase representa la ventana de la aplicacion
    """

    def __init__(self):
        """
            Constructor de la clase View que inicializa los atributos:
            display, clock, background, font
        """
        self.tamaño = (460,500)
        self.display = pygame.display.set_mode(self.tamaño)
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.background = None
        self.font = pygame.font.Font(None, 36)

    def drawMenu(self, buttons):
        """
            Este metodo dibuja el menu
        """
        self.ChooseTam(600)
        image = pygame.image.load("images/CULEBRA.jpg")
        self.display.fill((217, 213, 147))
        self.display.blit(image, (0, 25))
        buttons.draw(self.display)
        pygame.display.flip()

    def drawGame(self, objects, speed, score, contFruit):
        """
            Este metodo dibuja la ventana de juego
        """
        self.ChooseTam(500)
        text = "Score: " + str(score)
        scoreText = self.font.render(text, True, (201, 10, 0))
        text = "Speed: " + str(speed)
        speedText = self.font.render(text, True, (201, 10, 0))
        text = "Fruits: " + str(contFruit)
        contText = self.font.render(text, True, (201, 10, 0))
        self.display.fill(WHITE)
        
        self.background = pygame.image.load("images/background.png")

        self.display.blit(self.background,(0, 0))     
        self.display.blit(scoreText, (15, 25))
        self.display.blit(speedText, (185, 25))
        self.display.blit(contText, (315, 25))

        for object_ in objects:

            object_.draw(self.display)        
        
        pygame.display.flip()
        self.clock.tick(speed)

    def drawGameOver(self, buttons):
        """
            Este metodo dibuja la ventana de game Over
        """
        self.ChooseTam(500)
        self.display.fill(WHITE)
        self.background = pygame.image.load("images/bg_game_over.png")
        self.display.blit(self.background,(0,0))
        buttons.draw(self.display)
        pygame.display.flip()

    def drawPaused(self, buttons):
        """
            Este metodo dibuja la ventana de pausa
        """
        self.ChooseTam(500)
        self.display.fill(WHITE)
        self.background = pygame.image.load("images/bg_pause.png")
        self.display.blit(self.background,(0,0))
        buttons.draw(self.display)
        pygame.display.flip()

    def drawLoad(self, buttons):
        text = self.font.render("Select a Game Mode", True, (255, 0, 0))
        self.ChooseTam(420)
        self.display.fill((217, 213, 147))
        self.display.blit(text, (100, 60))
        buttons.draw(self.display)
        pygame.display.flip()

    def drawScores(self, buttons, p1, p2, p3, p4, p5):
        """
        Mostrar los puntajes en una ventana separada.
        """
        self.background = pygame.image.load("images/bg_scores.png")
        self.ChooseTam(500)
        text = "Score 1: " + str(p1)
        score1Text = self.font.render(text, True, (69, 43, 52))
        text = "Score 2: " + str(p2)
        score2Text = self.font.render(text, True, (69, 43, 52))
        text = "Score 3: " + str(p3)
        score3Text = self.font.render(text, True, (69, 43, 52))
        text = "Score 4: " + str(p4)
        score4Text = self.font.render(text, True, (69, 43, 52))
        text = "Score 5: " + str(p5)
        score5Text = self.font.render(text, True, (69, 43, 52))
        self.display.fill(WHITE)

        self.display.blit(self.background,(0, 0)) 

        self.display.blit(score1Text, (165, 125))
        self.display.blit(score2Text, (165, 175))
        self.display.blit(score3Text, (165, 225))
        self.display.blit(score4Text, (165, 275))
        self.display.blit(score5Text, (165, 325))

        buttons.draw(self.display)
        pygame.display.flip()

    def drawCredits(self, buttons):
        self.ChooseTam(500)
        credits_text = [
        "Desarrollado por: ",
        "",
        "Juan Pablo Sotelo",
        "Juan David Pulido",
        "Daniel Felipe Sanchez",
          
        "Gracias por jugar!",
       
        ]

        font = pygame.font.Font(None, 50)
        y_offset = 100  # Ajusta la posición vertical de cada línea de texto

        self.display.fill((217, 213, 147))

        for line in credits_text:
            text = font.render(line, True, ((255, 0, 0)))  # Renderiza el texto
            text_rect = text.get_rect(center=(230, y_offset))  # Centra el texto horizontalmente
            self.display.blit(text, text_rect)  
            y_offset += 50  
        
        buttons.draw(self.display)
        pygame.display.flip()  

    def ChooseTam(self, y):
        if(self.tamaño != (460, y)):
            self.tamaño = (460, y)
            self.display = pygame.display.set_mode(self.tamaño)
