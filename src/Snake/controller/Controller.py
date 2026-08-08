import pickle
import sys

import pygame

from controller.AudioController import AudioController
from controller.GameController import GameController
from controller.gameControllerAdapter import GameControllerAdapter
from model.Button import Button
from paths import data_path, image_path, sound_path

class Controller:

    def __init__(self, view) -> None:
        
        self.audio = AudioController()
        self.view = view
        self.gameController = GameController(self.view, self.audio)
        self.adapter = GameControllerAdapter(self.gameController)
        self.game = None
        self.menu = True
        self.musicMenu = sound_path("menu-music-28480.mp3")
        self.musicGame = sound_path("8bit-sample-69080.mp3")
        self.buttons = pygame.sprite.Group()
        self.scores = [0] * 5

    def handleMenuEvents(self):
        """
            Esta clase maneja los eventos de la pantalla del menú
        """
        self.audio.repMusic(self.musicMenu)
        self.loadScores()
        while True:


            # Creacion de los botones del menú
            self.buttons.remove(self.buttons)
            buttonPlay = Button(100, 148, image_path("btn_play1.png"), 255, 69)
            buttonPlay2 = Button(100, 232, image_path("btn_play2.png"), 255, 69)
            buttonLoad = Button(100, 316, image_path("btn_load.png"), 255, 69)
            buttonScore = Button(100, 400, image_path("btn_score.png"), 255, 69)
            buttonCredits = Button(100, 484, image_path("btn_credits.png"), 255, 69)
            self.buttons.add([buttonPlay, buttonPlay2, buttonLoad, buttonScore, buttonCredits])
            
            # Escucha si el mouse esta sobre algun boton
            for button in self.buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.itsHover()
                else:
                    button.itsNormal()
            
            # Escucha los eventos del teclado y mouse
            for event in pygame.event.get():
                # Cierra el juego
                if event.type == pygame.QUIT:
                    self.closeGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Escucha si el usuario presiono algun boton
                    mouse_pos = pygame.mouse.get_pos()
                    if 100 <= mouse_pos[0] < 355:
                        if 148 <= mouse_pos[1] < 217:
                            # Iniciar nuevo juego
                            self.game = self.gameController
                            self.game.newGame()
                            self.startGame()
                        elif 232 <= mouse_pos[1] < 301:
                            # Iniciar nuevo juego modo 2.0
                            self.game = self.adapter
                            self.game.newGame()
                            self.startGame()
                        elif 316 <= mouse_pos[1] < 385:
                            self.menu = False
                            self.handleLoadEvents()
                        elif 400 <= mouse_pos[1] < 469:
                            # Mostrar Puntajes
                            self.menu = False
                            self.handleScoresEvents()                        
                        elif 484 <= mouse_pos[1] < 553:
                            self.menu = False
                            self.showCredits()
            
            # Dibujar los botones en el menú
            self.view.drawMenu(self.buttons)
    
    def handleGameEvents(self):
        # Escucha los eventos del teclado y mouse
        for event in pygame.event.get():
            # Cierra el juego
            if(event.type == pygame.QUIT):
                self.closeGame()
            if(event.type == pygame.KEYDOWN):
                # Escucha si se puso en pausa
                if(event.key == pygame.K_ESCAPE):
                    self.game.paused = True

                # Escucha si se movio el Snake
                else:
                    self.game.setSpeeds(event)
                
        self.game.key = False

    def startGame(self):
        
        """
            Este es el metodo donde esta la logica del juego
        """

        # Se da inicio a la musica del juego
        self.audio.repMusic(self.musicGame)

        self.menu = False

        # Game loop
        while(not self.game.gameOver and not self.menu):
            if self.game.paused != True:
                self.handleGameEvents()
                self.game.startGame()
            else:
                self.handlePausedEvents()
        
        pygame.mixer.music.stop()
        if(self.game.gameOver == True):
            self.updateScores(self.gameController.score)
            self.audio.repSound(pygame.mixer.Sound(sound_path("gameOver.mp3")))   

        while not self.menu:
            
            self.handleGameOverEvents()
        
        self.audio.repMusic(self.musicMenu)

    def handlePausedEvents(self):

        """
            Este metodo se encarga del manejo de los eventos del menu de pausa
        """

        # Creacion de los botones del menú
        self.buttons.remove(self.buttons)
        buttonResume = Button(91, 163, image_path("btn_continue.png"), 280, 69)
        buttonSave = Button(91, 252, image_path("btn_save.png"), 280, 69)
        buttonMenu = Button(91, 341, image_path("btn_menu.png"), 280, 69)
        
        self.buttons.add([buttonResume, buttonSave, buttonMenu])
    
        # Escucha si el mouse esta sobre algun boton
        for button in self.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.itsHover()
            else:
                button.itsNormal()

        # Escucha los eventos del teclado
        for event in pygame.event.get():
            #Cierra el juego
            if event.type == pygame.QUIT:
                self.closeGame()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 91 <= mouse_pos[0] < 371:
                    if 163 <= mouse_pos[1] < 232:
                        # Volver al juego
                        self.game.paused = False
                    elif 252 <= mouse_pos[1] < 321:
                        # Guardar Partida
                        self.game.saveGame()
                        pass
                    elif 341 <= mouse_pos[1] < 410:
                        # Volver al menu
                        self.menu = True

        self.view.drawPaused(self.buttons)

    def handleGameOverEvents(self):
        """
            Este metodo se encarga del manejo de los eventos del menu de pausa
        """

        # Creacion de los botones del GameOver
        self.buttons.remove(self.buttons)
        buttonYes = Button(33, 375, image_path("btn_yes.png"), 187, 69)
        buttonNo = Button(241, 375, image_path("btn_no.png"), 187, 69)
        self.buttons.add([buttonYes, buttonNo])
            
        # Escucha si el mouse esta sobre algun boton
        for button in self.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.itsHover()
            else:
                button.itsNormal()

        # Escucha los eventos del teclado
        for event in pygame.event.get():
            #Cierra el juego
            if event.type == pygame.QUIT:
                self.closeGame()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 375 <= mouse_pos[1] < 444:
                    if 33 <= mouse_pos[0] < 220:
                        # Jugar de nuevo
                        self.audio.stopChannel()
                        self.menu = True
                        self.game.newGame()
                        self.startGame()
                    elif 241 <= mouse_pos[0] < 428:
                        # Salir al menu
                        self.audio.stopChannel()
                        self.menu = True
        
        self.view.drawGameOver(self.buttons)

    def handleLoadEvents(self):
        #Creacion de los botones del Load
        self.buttons.remove(self.buttons)
        buttonLoad1 = Button(91, 120, image_path("btn_play1.png"), 255, 69)
        buttonLoad2 = Button(91, 209, image_path("btn_play2.png"), 255, 69)
        buttonBack = Button(91, 298, image_path("btn_back.png"), 255, 69)
        self.buttons.add([buttonLoad1, buttonLoad2, buttonBack])

        

        # Escucha los eventos del teclado
        while not self.menu:
            # Escucha si el mouse esta sobre algun boton
            for button in self.buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.itsHover()
                else:
                    button.itsNormal()
                    
            for event in pygame.event.get():
                #Cierra el juego
                if event.type == pygame.QUIT:
                    self.closeGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Escucha si el usuario presiono algun boton
                    mouse_pos = pygame.mouse.get_pos()
                    if 91 <= mouse_pos[0] < 346:
                        if 120 <= mouse_pos[1] < 189:
                            # Cargar Partida 1.0
                            self.game = self.gameController
                            self.game.loadGame()
                            self.startGame()
                        elif 209 <= mouse_pos[1] < 278:
                            # Cargar Partida 2.0
                            self.game = self.adapter
                            self.game.loadGame()
                            self.startGame()
                        elif 298 <= mouse_pos[1] < 367:
                            self.menu = True

            self.view.drawLoad(self.buttons)

    def handleScoresEvents(self):
        """
            Este metodo se encarga del manejo de los eventos del menu de scores
        """

        # Creacion de los botones del menú
        self.buttons.remove(self.buttons)
        buttonBack = Button(104, 413, image_path("btn_back.png"), 255, 69)
        
        self.buttons.add([buttonBack])

        while(not self.menu):
            # Escucha si el mouse esta sobre algun boton
            for button in self.buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.itsHover()
                else:
                    button.itsNormal()

            # Escucha los eventos del teclado
            for event in pygame.event.get():
                #Cierra el juego
                if event.type == pygame.QUIT:
                    self.closeGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 413 <= mouse_pos[1] < 482:
                        if 125 <= mouse_pos[0] < 379:
                            self.menu = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.menu = True
            
            # Ordenar los puntajes de mayor a menor
            sorted_scores = sorted(self.scores, reverse=True)

            # Obtener los 5 puntajes
            p1, p2, p3, p4, p5 = sorted_scores[:5]

            self.view.drawScores(self.buttons, p1, p2, p3, p4, p5)

    def showCredits(self): 
        """
            Este metodo se encarga del manejo de los eventos del menu de scores
        """

        # Creacion de los botones del menú
        self.buttons.remove(self.buttons)
        buttonBack = Button(104, 413, image_path("btn_back.png"), 255, 69)
        
        self.buttons.add([buttonBack])

        while not self.menu:
            # Escucha si el mouse esta sobre algun boton
            for button in self.buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.itsHover()
                else:
                    button.itsNormal()

            # Escucha los eventos del teclado
            for event in pygame.event.get():
                #Cierra el juego
                if event.type == pygame.QUIT:
                    self.closeGame()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 413 <= mouse_pos[1] < 482:
                        if 125 <= mouse_pos[0] < 379:
                            self.menu = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu = True
                           
            self.view.drawCredits(self.buttons)

    

    def saveScores(self):
        data = {'scores' : self.scores}

        file = data_path("scores.pkl")

        with open(file, 'wb') as f:
            pickle.dump(data, f)

    def loadScores(self):

        file = data_path("scores.pkl")

        try:
            with open(file, 'rb') as f:
                data = pickle.load(f)
            self.scores = data['scores']
        except (FileNotFoundError, KeyError, pickle.UnpicklingError):
            self.scores = [0] * 5

    def updateScores(self, new_score):
        """
        Actualizar la lista de puntajes con un nuevo puntaje.
        """
        # Agregar el nuevo puntaje a la lista si es mayor que el mínimo actual
        if new_score > min(self.scores):
            self.scores[self.scores.index(min(self.scores))] = new_score
            # Ordenar la lista de puntajes de mayor a menor
            self.scores.sort(reverse=True)

    def closeGame(self):
        self.saveScores()
        pygame.quit()
        sys.exit()