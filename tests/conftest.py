import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import pytest
from config import GAME_HEIGHT, WINDOW_WIDTH
from controller.game_controller import GameController


class _FakeSound:
    """Reemplaza pygame.mixer.Sound para no depender de decodificación de audio."""

    def __init__(self, *args, **kwargs):
        pass


class FakeView:
    """Vista simulada que no dibuja nada."""

    def drawGame(self, objects, speed, score, contFruit):
        pass


class FakeAudio:
    """Controlador de audio simulado."""

    def repSound(self, sound):
        pass


@pytest.fixture(scope="session", autouse=True)
def pygame_display():
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, GAME_HEIGHT))
    if hasattr(pygame, "mixer"):
        pygame.mixer.Sound = _FakeSound
    yield
    pygame.quit()


@pytest.fixture
def view():
    return FakeView()


@pytest.fixture
def audio():
    return FakeAudio()


@pytest.fixture
def game_controller(view, audio):
    return GameController(view, audio)
