import pygame


class AudioController:
    def __init__(self) -> None:
        self.channel = pygame.mixer.Channel(0)

    def stopChannel(self):
        self.channel.stop()

    def repSound(self, sound):
        self.channel.stop()  # Detener cualquier reproducción anterior en el mismo canal
        self.channel.play(sound)  # Reproducir el sonido proporcionado
        self.channel.set_volume(1)

    def repMusic(self, music):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(1)
