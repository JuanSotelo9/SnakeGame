import pygame
from config import (
    CREDITS_CENTER_X,
    CREDITS_FONT_SIZE,
    CREDITS_LINE_SPACING,
    CREDITS_START_Y,
    FRUITS_TEXT_POS,
    GAME_HEIGHT,
    HUD_FONT_SIZE,
    HUD_TEXT_COLOR,
    LOAD_SCREEN_HEIGHT,
    LOAD_TEXT_POS,
    MENU_BACKGROUND_COLOR,
    MENU_HEIGHT,
    MENU_IMAGE_POS,
    SCORE_TEXT_COLOR,
    SCORE_TEXT_POS,
    SCORES_LINE_SPACING,
    SCORES_START_Y,
    SCORES_TEXT_X,
    SPEED_TEXT_POS,
    TITLE_TEXT_COLOR,
    WHITE,
    WINDOW_WIDTH,
)
from paths import image_path


class View:
    """
    Esta clase representa la ventana de la aplicacion
    """

    def __init__(self):
        """
        Constructor de la clase View que inicializa los atributos:
        display, clock, background, font
        """
        self.tamaño = (WINDOW_WIDTH, GAME_HEIGHT)
        self.display = pygame.display.set_mode(self.tamaño)
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.background = None
        self.font = pygame.font.Font(None, HUD_FONT_SIZE)

    def drawMenu(self, buttons):
        """
        Este metodo dibuja el menu
        """
        self.ChooseTam(MENU_HEIGHT)
        image = pygame.image.load(image_path("CULEBRA.jpg"))
        self.display.fill(MENU_BACKGROUND_COLOR)
        self.display.blit(image, MENU_IMAGE_POS)
        buttons.draw(self.display)
        pygame.display.flip()

    def drawGame(self, objects, speed, score, contFruit):
        """
        Este metodo dibuja la ventana de juego
        """
        self.ChooseTam(GAME_HEIGHT)
        scoreText = self.font.render("Score: " + str(score), True, HUD_TEXT_COLOR)
        speedText = self.font.render("Speed: " + str(speed), True, HUD_TEXT_COLOR)
        contText = self.font.render("Fruits: " + str(contFruit), True, HUD_TEXT_COLOR)
        self.display.fill(WHITE)

        self.background = pygame.image.load(image_path("background.png"))

        self.display.blit(self.background, (0, 0))
        self.display.blit(scoreText, SCORE_TEXT_POS)
        self.display.blit(speedText, SPEED_TEXT_POS)
        self.display.blit(contText, FRUITS_TEXT_POS)

        for object_ in objects:
            object_.draw(self.display)

        pygame.display.flip()
        self.clock.tick(speed)

    def drawGameOver(self, buttons):
        """
        Este metodo dibuja la ventana de game Over
        """
        self.ChooseTam(GAME_HEIGHT)
        self.display.fill(WHITE)
        self.background = pygame.image.load(image_path("bg_game_over.png"))
        self.display.blit(self.background, (0, 0))
        buttons.draw(self.display)
        pygame.display.flip()

    def drawPaused(self, buttons):
        """
        Este metodo dibuja la ventana de pausa
        """
        self.ChooseTam(GAME_HEIGHT)
        self.display.fill(WHITE)
        self.background = pygame.image.load(image_path("bg_pause.png"))
        self.display.blit(self.background, (0, 0))
        buttons.draw(self.display)
        pygame.display.flip()

    def drawLoad(self, buttons):
        text = self.font.render("Select a Game Mode", True, TITLE_TEXT_COLOR)
        self.ChooseTam(LOAD_SCREEN_HEIGHT)
        self.display.fill(MENU_BACKGROUND_COLOR)
        self.display.blit(text, LOAD_TEXT_POS)
        buttons.draw(self.display)
        pygame.display.flip()

    def drawScores(self, buttons, p1, p2, p3, p4, p5):
        """
        Mostrar los puntajes en una ventana separada.
        """
        self.background = pygame.image.load(image_path("bg_scores.png"))
        self.ChooseTam(GAME_HEIGHT)
        scores = (p1, p2, p3, p4, p5)
        self.display.fill(WHITE)

        self.display.blit(self.background, (0, 0))

        for i, score in enumerate(scores):
            text = self.font.render(f"Score {i + 1}: {score}", True, SCORE_TEXT_COLOR)
            self.display.blit(text, (SCORES_TEXT_X, SCORES_START_Y + i * SCORES_LINE_SPACING))

        buttons.draw(self.display)
        pygame.display.flip()

    def drawCredits(self, buttons):
        self.ChooseTam(GAME_HEIGHT)
        credits_text = [
            "Desarrollado por: ",
            "",
            "Juan Pablo Sotelo",
            "Juan David Pulido",
            "Daniel Felipe Sanchez",
            "Gracias por jugar!",
        ]

        font = pygame.font.Font(None, CREDITS_FONT_SIZE)
        y_offset = CREDITS_START_Y

        self.display.fill(MENU_BACKGROUND_COLOR)

        for line in credits_text:
            text = font.render(line, True, TITLE_TEXT_COLOR)
            text_rect = text.get_rect(center=(CREDITS_CENTER_X, y_offset))
            self.display.blit(text, text_rect)
            y_offset += CREDITS_LINE_SPACING

        buttons.draw(self.display)
        pygame.display.flip()

    def ChooseTam(self, y):
        if self.tamaño != (WINDOW_WIDTH, y):
            self.tamaño = (WINDOW_WIDTH, y)
            self.display = pygame.display.set_mode(self.tamaño)
