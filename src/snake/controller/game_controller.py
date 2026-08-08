import pickle
import random

import pygame
from config import (
    BOARD_MAX_COL,
    BOARD_MAX_ROW,
    BOARD_MIN_COL,
    BOARD_MIN_ROW,
    INITIAL_SPEED,
    MAX_SPEED,
    SCORE_PER_FRUIT,
    SPEED_UP_EVERY,
    SPRITE_SIZE,
    START_HEAD_X,
    START_HEAD_Y,
)
from controller.game_controller_interface import GameControllerInterface
from model.body import Body
from model.fruit import Fruit
from paths import data_path, image_path, sound_path


class GameController(GameControllerInterface):
    def __init__(self, view, audio):
        """
        Constructor de la clase GameController que inicializa los atributos:
        view, speedGame, gameOver, sizeSprite, speedX, speedY, head, existsFruit,
        fruitPosX, fruitPosY, contFruit, parts, fruit, snake, paused, menu,
        music, buttons
        """
        self.view = view
        self.audio = audio
        self.speedGame = INITIAL_SPEED  # Guardar
        self.sizeSprite = SPRITE_SIZE
        self.speedX = 0
        self.speedY = 0
        self.head = Body(START_HEAD_X, START_HEAD_Y, image_path("head.png"))
        self.existsFruit = False
        self.fruitPosX = -1  # Guardar
        self.fruitPosY = -1  # Guardar
        self.contFruit = 0  # Guardar
        self.parts = []  # Guardar
        self.fruit = pygame.sprite.GroupSingle()
        self.snake = pygame.sprite.Group()
        self.parts.append(self.head)
        self.snake.add(self.head)
        self.score = 0  # Guardar
        self.paused = False
        self.gameOver = False
        self.key = False

    def newGame(self):
        """
        Este metodo inicializa los valores para una nueva partida
        """
        self.gameOver = False
        self.speedGame = INITIAL_SPEED
        self.speedX = 0
        self.speedY = 0
        self.head = Body(START_HEAD_X, START_HEAD_Y, image_path("head.png"))
        self.existsFruit = False
        self.fruitPosX = -1
        self.fruitPosY = -1
        self.contFruit = 0
        self.parts.clear()
        self.fruit.remove(self.fruit)
        self.snake.remove(self.snake)
        self.parts.append(self.head)
        self.snake.add(self.head)
        self.paused = False
        self.score = 0
        self.key = False

    def startGame(self):
        """
        Este es el metodo donde esta la logica del juego
        """
        if self.paused != True:
            # Comprueba colision de la cabeza con la fruta
            if self.head.rect.x == self.fruitPosX and self.head.rect.y == self.fruitPosY:
                # Crea una nueva parte del cuerpo
                self.audio.repSound(pygame.mixer.Sound(sound_path("comer.mp3")))
                self.addBody()
                self.existsFruit = False

            # Comprueba si no hay frutas en el tablero
            if self.existsFruit == False:
                # Se crea una nueva fruta
                self.fruit.add(self.createFruit(image_path("fruit1.png")))
                self.existsFruit = True

            # Mueve el Snake
            self.moveSnake()

            # Verifica si hay game Over
            if self.speedX != 0 or self.speedY != 0:
                self.gameOver = self.itsGameOver()

            if self.gameOver != True:
                self.view.drawGame(
                    [self.fruit, self.snake], self.speedGame, self.score, self.contFruit
                )

    def setSpeeds(self, event):
        """
        Este metodo asigna las velocidades segun la tecla presionada
        """
        if not self.key:
            if (
                event.key == pygame.K_DOWN or event.key == pygame.K_s
            ) and self.speedY != -1 * self.sizeSprite:
                self.speedY = self.sizeSprite
                self.speedX = 0
                self.key = True
            if (
                event.key == pygame.K_UP or event.key == pygame.K_w
            ) and self.speedY != self.sizeSprite:
                self.speedY = -1 * self.sizeSprite
                self.speedX = 0
                self.key = True
            if (
                event.key == pygame.K_LEFT or event.key == pygame.K_a
            ) and self.speedX != self.sizeSprite:
                self.speedX = -1 * self.sizeSprite
                self.speedY = 0
                self.key = True
            if (
                event.key == pygame.K_RIGHT or event.key == pygame.K_d
            ) and self.speedX != -1 * self.sizeSprite:
                self.speedX = self.sizeSprite
                self.speedY = 0
                self.key = True

    def addBody(self):
        """
        Este metodo crea una nueva parte del snake
        """
        part = self.parts[-1]
        speed = part.getSpeed()
        bodyimg = image_path("body.png")
        if speed[0] == 0:
            if speed[1] == self.sizeSprite:
                body = Body(part.rect.x, part.rect.y - self.sizeSprite, bodyimg)
            else:
                body = Body(part.rect.x, part.rect.y + self.sizeSprite, bodyimg)
        else:
            if speed[0] == self.sizeSprite:
                body = Body(part.rect.x - self.sizeSprite, part.rect.y, bodyimg)
            else:
                body = Body(part.rect.x + self.sizeSprite, part.rect.y, bodyimg)
        self.parts.append(body)
        self.snake.add(body)
        self.contFruit += 1
        self.score += SCORE_PER_FRUIT * self.speedGame
        if (
            self.contFruit % SPEED_UP_EVERY == 0
            and self.contFruit != 0
            and self.speedGame < MAX_SPEED
        ):
            self.speedGame += 1

    def createFruit(self, typeFruit) -> Fruit:
        """
        Este metodo se encarga de crear una fruta
        """
        while True:
            self.fruitPosX = random.randint(BOARD_MIN_COL, BOARD_MAX_COL) * SPRITE_SIZE
            self.fruitPosY = random.randint(BOARD_MIN_ROW, BOARD_MAX_ROW) * SPRITE_SIZE
            if self.itsAvailable(self.fruitPosX, self.fruitPosY) == True:
                break
        return Fruit(self.fruitPosX, self.fruitPosY, typeFruit)

    def itsAvailable(self, x, y) -> bool:
        for part in self.parts:
            if part.rect.x == x and part.rect.y == y:
                return False

        return True

    def moveSnake(self):
        """
        Este metodo se encarga de mover todas las partes del snake
        """

        prevSpeed = [0, 0]
        for part in self.parts:
            aux = part.getSpeed()
            if prevSpeed[0] == 0 and prevSpeed[1] == 0:
                part.setSpeed(self.speedX, self.speedY)
                part.move()
            else:
                part.setSpeed(prevSpeed[0], prevSpeed[1])
                part.move()

            prevSpeed = aux

    def itsGameOver(self):
        """
        Este metodo revisa si hubo game over
        """
        if (
            self.head.rect.x < SPRITE_SIZE
            or self.head.rect.x > BOARD_MAX_COL * SPRITE_SIZE
            or self.head.rect.y < BOARD_MIN_ROW * SPRITE_SIZE
            or self.head.rect.y > BOARD_MAX_ROW * SPRITE_SIZE
        ):
            return True
        else:
            for part in self.parts:
                if (
                    self.head.rect.x == part.rect.x
                    and self.head.rect.y == part.rect.y
                    and part != self.head
                ):
                    return True

        return False

    def saveGame(self):

        snake = {}
        for index, part in enumerate(self.parts):
            snake[index] = [part.speedx, part.speedy, part.rect.x, part.rect.y]

        data = {
            "snake": snake,
            "speedGame": self.speedGame,
            "fruitPosX": self.fruitPosX,
            "fruitPosY": self.fruitPosY,
            "contFruit": self.contFruit,
            "score": self.score,
        }

        file = data_path("save_game.pkl")

        with open(file, "wb") as f:
            pickle.dump(data, f)

    def loadGame(self):

        file = data_path("save_game.pkl")

        try:
            with open(file, "rb") as f:
                data = pickle.load(f)
        except (FileNotFoundError, KeyError, pickle.UnpicklingError):
            self.newGame()
            return

        self.gameOver = False
        self.speedGame = data["speedGame"]
        self.existsFruit = True
        self.fruitPosX = data["fruitPosX"]
        self.fruitPosY = data["fruitPosY"]
        self.contFruit = data["contFruit"]
        self.score = data["score"]
        self.paused = True
        self.parts.clear()
        self.fruit.remove(self.fruit)
        self.snake.remove(self.snake)
        self.fruit.add(Fruit(self.fruitPosX, self.fruitPosY, image_path("fruit1.png")))
        snake = data["snake"]

        for key in snake:
            part = snake[key]
            if key == 0:
                self.speedX = part[0]
                self.speedY = part[1]
                self.head = Body(part[2], part[3], image_path("head.png"))
                self.head.setSpeed(part[0], part[1])
                self.parts.append(self.head)
                self.snake.add(self.head)
            else:
                body = Body(part[2], part[3], image_path("body.png"))
                body.setSpeed(part[0], part[1])
                self.parts.append(body)
                self.snake.add(body)
