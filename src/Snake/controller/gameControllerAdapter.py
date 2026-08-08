import pickle
import random

import pygame

from controller.GameController import GameController
from model.Body import Body
from model.Fruit import Fruit
from model.Wall import Wall
from paths import data_path, image_path, sound_path

class GameControllerAdapter:

    def __init__(self, gameController: GameController) -> None:
        self.gameController = gameController
        self.audio = gameController.audio
        self.gameOver = False
        self.paused = False
        self.wallPosX = -1
        self.wallPosY = -1
        self.contWall = 0 # Guardar
        self.walls = [] # Guardar
        self.wallSprites = pygame.sprite.Group()
        self.fruitType = 0
        self.chooseFruit = None
        self.key = self.gameController.key
    
    def newGame(self):
        self.gameController.newGame()
        self.wallPosX = -1
        self.wallPosY = -1
        self.contWall = 0 # Guardar
        self.walls.clear()
        self.wallSprites.remove(self.wallSprites)
        self.gameOver = False
        self.paused = False
        self.fruitType = 0
    
    def startGame(self):
        """
            Este es el metodo donde esta la logica del juego
        """

        if(self.paused != True):

            # Comprueba colision de la cabeza con la fruta
            if(self.gameController.head.rect.x == self.gameController.fruitPosX and 
               self.gameController.head.rect.y == self.gameController.fruitPosY):
                # Crea una nueva parte del cuerpo
                self.audio.repSound(pygame.mixer.Sound(sound_path("comer.mp3")))
                self.gameController.addBody()
                if(self.gameController.contFruit % 2 == 0):
                    self.createWall()
                if(self.chooseFruit == "fruit1"):
                    self.fruitType = 1
                elif(self.chooseFruit == "fruit2"):
                    self.fruitType = 2
                    self.gameController.score += 1*self.gameController.speedGame
                elif(self.chooseFruit == "fruit3"):
                    self.fruitType = 3
                elif(self.chooseFruit == "fruit4"):
                    self.fruitType = 4 
                self.gameController.existsFruit = False

            # Comprueba si no hay frutas en el tablero
            if(self.gameController.existsFruit == False):
                # Se crea una nueva fruta
                self.gameController.fruit.add(self.createFruit())
                self.gameController.existsFruit = True

            # Mueve el Snake
            self.gameController.moveSnake()

            # Verifica si hay game Over
            if(self.gameController.speedX != 0 or self.gameController.speedY != 0):
                self.gameOver = self.itsGameOver()

            if(self.gameOver != True):
                self.gameController.view.drawGame([self.gameController.fruit, self.gameController.snake, self.wallSprites], 
                                   self.gameController.speedGame, self.gameController.score, self.gameController.contFruit)

    def setSpeeds(self, event):
        
        if(self.fruitType == 4):
            if(not self.key):
                if((event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.gameController.speedY != self.gameController.sizeSprite):
                    self.gameController.speedY = -1*self.gameController.sizeSprite
                    self.gameController.speedX = 0
                    self.key = True
                if((event.key == pygame.K_UP or event.key == pygame.K_w) and self.gameController.speedY != -1*self.gameController.sizeSprite):
                    self.gameController.speedY = self.gameController.sizeSprite
                    self.gameController.speedX = 0
                    self.key = True
                if((event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.gameController.speedX != -1*self.gameController.sizeSprite):
                    self.gameController.speedX = self.gameController.sizeSprite
                    self.gameController.speedY = 0
                    self.key = True
                if((event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.gameController.speedX != self.gameController.sizeSprite):
                    self.gameController.speedX = -1*self.gameController.sizeSprite
                    self.gameController.speedY = 0
                    self.key = True
        else:
            self.gameController.key = self.key
            self.gameController.setSpeeds(event)

    def createWall(self):
        """
            Este metodo se encarga de crear un muro
        """
        while(True):
            self.wallPosX = random.randint(1,21)*20
            self.wallPosY = random.randint(4,23)*20
            if(self.itsAvailableWall(self.wallPosX, self.wallPosY) == True):
                break;
        wall = Wall(self.wallPosX, self.wallPosY, image_path("wall.png"))
        self.walls.append(wall)
        self.wallSprites.add(wall)
        self.contWall += 1
    
    def itsAvailableWall(self, x, y) -> bool:
        for part in self.gameController.parts:
            if(part.rect.x == x and part.rect.y == y):
                return False
            
        headPosX = self.gameController.head.rect.x // self.gameController.sizeSprite
        headPosY = self.gameController.head.rect.y // self.gameController.sizeSprite
        wallPosX = x // self.gameController.sizeSprite
        wallPosY = y // self.gameController.sizeSprite
        if(abs(headPosX - wallPosX) < 10 and abs(headPosY - wallPosY) < 10):
            return False
        
        for wall in self.walls:
            if(wall.rect.x == x and wall.rect.y == y):
                return False
            
        if(x == self.gameController.fruitPosX and y == self.gameController.fruitPosY):
            return False
        
        return True
    
    def destroyWall(self, wall):
        """
            Este metodo se encarga de destruir un muro
        """
        self.wallSprites.remove(wall)

    def createFruit(self) -> Fruit:
        self.chooseFruit = self.chooseFruits()
        fruit = image_path(f"{self.chooseFruit}.png")
        while True:
            aux = self.gameController.createFruit(fruit)
            if(self.itsAvailable(self.gameController.fruitPosX, self.gameController.fruitPosY)):
                break;
        
        return aux
    
    def itsAvailable(self, x, y) -> bool:
        if not self.walls:
            return True

        for wall in self.walls:
            if wall.rect.x == x and wall.rect.y == y:
                return False
        
        return True
    
    
    def chooseFruits(self):
        randomNum = random.uniform(0, 1)

        probabilities = {
            "fruit1": 0.75,
            "fruit2": 0.15,
            "fruit3": 0.01,
            "fruit4": 0.09
        }

        lower_limit = 0

        for fruit, probability in probabilities.items():
            # Actualizar el limite superior de la probabilidad acumulada
            upper_limit = lower_limit + probability

            # Si el número aleatorio esta dentro del rango de esta opcion, es seleccionado
            if lower_limit <= randomNum < upper_limit:
                return fruit
            
            # Actualizar el limite inferior
            lower_limit = upper_limit

    def itsGameOver(self) -> bool:
        for wall in self.walls:
            # Comprueba colision de la cabeza con un muro
            if(self.gameController.head.rect.x == wall.rect.x and self.gameController.head.rect.y == wall.rect.y):
                if(self.fruitType != 3):
                    return True
                else:
                    self.destroyWall(wall)
                    self.walls.remove(wall)

        return self.gameController.itsGameOver()


    def saveGame(self):
        snake = {}
        wallsG = {}
        index = 0
        for part in self.gameController.parts:
            snake[index] = [part.speedx, part.speedy, part.rect.x, part.rect.y]
            index += 1

        index = 0
        for wall in self.walls:
            wallsG[index] = [wall.rect.x, wall.rect.y]
            index += 1

        data = {'snake' : snake, 'speedGame' : self.gameController.speedGame, 'fruitPosX' : self.gameController.fruitPosX, 
                'fruitPosY' : self.gameController.fruitPosY, 'contFruit' : self.gameController.contFruit, 
                'score' : self.gameController.score, 'wallsG' : wallsG, 'contWall' : self.contWall, 'fruitType' : self.fruitType}
        
        file = data_path("save_game2.0.pkl")

        with open(file, "wb") as f:
            pickle.dump(data,f)

    def loadGame(self):
        file = data_path("save_game2.0.pkl")

        try:
            with open(file, 'rb') as f:
                data = pickle.load(f)
        except (FileNotFoundError, KeyError, pickle.UnpicklingError):
            self.newGame()
            return

        self.gameOver = False
        self.gameController.speedGame = data['speedGame']
        self.gameController.existsFruit = True
        self.gameController.fruitPosX = data['fruitPosX']
        self.gameController.fruitPosY = data['fruitPosY']
        self.gameController.contFruit = data['contFruit']
        self.gameController.score = data['score']
        self.contWall = data["contWall"]
        self.paused = True
        self.gameController.parts.clear()
        self.gameController.fruit.remove(self.gameController.fruit)
        self.gameController.snake.remove(self.gameController.snake)
        self.gameController.fruit.add(Fruit(self.gameController.fruitPosX, self.gameController.fruitPosY, image_path("fruit1.png")))
        snake = data['snake']
        wallsG = data['wallsG']
        self.fruitType = data['fruitType']

        for key in snake:
            part = snake[key]
            if(key == 0):
                self.gameController.speedX = part[0]
                self.gameController.speedY = part[1]
                self.gameController.head = Body(part[2], part[3], image_path("head.png"))
                self.gameController.head.setSpeed(part[0], part[1])
                self.gameController.parts.append(self.gameController.head)
                self.gameController.snake.add(self.gameController.head)
            else:
                body = Body(part[2], part[3], image_path("body.png"))
                body.setSpeed(part[0], part[1])
                self.gameController.parts.append(body)
                self.gameController.snake.add(body)
        
        for key in wallsG:
            wall = Wall(wallsG[key][0], wallsG[key][1], image_path("wall.png"))
            self.walls.append(wall)
            self.wallSprites.add(wall)
