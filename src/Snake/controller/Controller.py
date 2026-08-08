import pickle
import sys

import pygame

from config import (
    BTN_BACK,
    BTN_GAMEOVER_NO,
    BTN_GAMEOVER_YES,
    BTN_LOAD_1,
    BTN_LOAD_2,
    BTN_LOAD_BACK,
    BTN_MENU_CREDITS,
    BTN_MENU_LOAD,
    BTN_MENU_PLAY,
    BTN_MENU_PLAY2,
    BTN_MENU_SCORE,
    BTN_PAUSE_MENU,
    BTN_PAUSE_RESUME,
    BTN_PAUSE_SAVE,
    MAX_SCORES,
)
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
        self.scores = [0] * MAX_SCORES

    def _create_button(self, layout, image_name):
        x, y, width, height = layout
        return Button(x, y, image_path(image_name), width, height)

    def handleMenuEvents(self):
        """
            Esta clase maneja los eventos de la pantalla del menú
        """
        self.audio.repMusic(self.musicMenu)
        self.loadScores()
        while True:


            # Creacion de los botones del menú
            self.buttons.remove(self.buttons)
            buttonPlay = self._create_button(BTN_MENU_PLAY, "btn_play1.png")
            buttonPlay2 = self._create_button(BTN_MENU_PLAY2, "btn_play2.png")
            buttonLoad = self._create_button(BTN_MENU_LOAD, "btn_load.png")
            buttonScore = self._create_button(BTN_MENU_SCORE, "btn_score.png")
            buttonCredits = self._create_button(BTN_MENU_CREDITS, "btn_credits.png")
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
                    if buttonPlay.rect.collidepoint(mouse_pos):
                        # Iniciar nuevo juego
                        self.game = self.gameController
                        self.game.newGame()
                        self.startGame()
                    elif buttonPlay2.rect.collidepoint(mouse_pos):
                        # Iniciar nuevo juego modo 2.0
                        self.game = self.adapter
                        self.game.newGame()
                        self.startGame()
                    elif buttonLoad.rect.collidepoint(mouse_pos):
                        self.menu = False
                        self.handleLoadEvents()
                    elif buttonScore.rect.collidepoint(mouse_pos):
                        # Mostrar Puntajes
                        self.menu = False
                        self.handleScoresEvents()
                    elif buttonCredits.rect.collidepoint(mouse_pos):
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
        buttonResume = self._create_button(BTN_PAUSE_RESUME, "btn_continue.png")
        buttonSave = self._create_button(BTN_PAUSE_SAVE, "btn_save.png")
        buttonMenu = self._create_button(BTN_PAUSE_MENU, "btn_menu.png")
        
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
                if buttonResume.rect.collidepoint(mouse_pos):
                    # Volver al juego
                    self.game.paused = False
                elif buttonSave.rect.collidepoint(mouse_pos):
                    # Guardar Partida
                    self.game.saveGame()
                elif buttonMenu.rect.collidepoint(mouse_pos):
                    # Volver al menu
                    self.menu = True

        self.view.drawPaused(self.buttons)

    def handleGameOverEvents(self):
        """
            Este metodo se encarga del manejo de los eventos del menu de pausa
        """

        # Creacion de los botones del GameOver
        self.buttons.remove(self.buttons)
        buttonYes = self._create_button(BTN_GAMEOVER_YES, "btn_yes.png")
        buttonNo = self._create_button(BTN_GAMEOVER_NO, "btn_no.png")
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
                if buttonYes.rect.collidepoint(mouse_pos):
                    # Jugar de nuevo
                    self.audio.stopChannel()
                    self.menu = True
                    self.game.newGame()
                    self.startGame()
                elif buttonNo.rect.collidepoint(mouse_pos):
                    # Salir al menu
                    self.audio.stopChannel()
                    self.menu = True
        
        self.view.drawGameOver(self.buttons)

    def handleLoadEvents(self):
        #Creacion de los botones del Load
        self.buttons.remove(self.buttons)
        buttonLoad1 = self._create_button(BTN_LOAD_1, "btn_play1.png")
        buttonLoad2 = self._create_button(BTN_LOAD_2, "btn_play2.png")
        buttonBack = self._create_button(BTN_LOAD_BACK, "btn_back.png")
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
                    if buttonLoad1.rect.collidepoint(mouse_pos):
                        # Cargar Partida 1.0
                        self.game = self.gameController
                        self.game.loadGame()
                        self.startGame()
                    elif buttonLoad2.rect.collidepoint(mouse_pos):
                        # Cargar Partida 2.0
                        self.game = self.adapter
                        self.game.loadGame()
                        self.startGame()
                    elif buttonBack.rect.collidepoint(mouse_pos):
                        self.menu = True

            self.view.drawLoad(self.buttons)

    def handleScoresEvents(self):
        """
            Este metodo se encarga del manejo de los eventos del menu de scores
        """

        # Creacion de los botones del menú
        self.buttons.remove(self.buttons)
        buttonBack = self._create_button(BTN_BACK, "btn_back.png")
        
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
                    if buttonBack.rect.collidepoint(pygame.mouse.get_pos()):
                        self.menu = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: 
                        self.menu = True
            
            # Ordenar los puntajes de mayor a menor
            sorted_scores = sorted(self.scores, reverse=True)

            # Obtener los mejores puntajes
            p1, p2, p3, p4, p5 = sorted_scores[:MAX_SCORES]

            self.view.drawScores(self.buttons, p1, p2, p3, p4, p5)

    def showCredits(self): 
        """
            Este metodo se encarga del manejo de los eventos del menu de scores
        """

        # Creacion de los botones del menú
        self.buttons.remove(self.buttons)
        buttonBack = self._create_button(BTN_BACK, "btn_back.png")
        
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
                    if buttonBack.rect.collidepoint(pygame.mouse.get_pos()):
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
            self.scores = [0] * MAX_SCORES

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