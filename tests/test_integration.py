import random

import pygame
import pytest
from config import (
    BOARD_MAX_COL,
    SCORE_PER_FRUIT,
    SPRITE_SIZE,
    START_HEAD_X,
    START_HEAD_Y,
)


def key_event(key):
    return pygame.event.Event(pygame.KEYDOWN, key=key)


def post_keys(*keys):
    for key in keys:
        pygame.event.post(key_event(key))


def play_frame(controller, *keys):
    """Simula un frame del bucle de juego: inyecta inputs y avanza la lógica."""
    post_keys(*keys)
    controller.handleGameEvents()
    controller.game.startGame()


def start_classic(controller):
    controller.game = controller.gameController
    controller.game.newGame()
    return controller.game


def start_adapter(controller):
    controller.game = controller.adapter
    controller.game.newGame()
    return controller.game


def eat_fruit(controller, game, choose_fruit=None, max_frames=3):
    """Coloca una fruta a la derecha de la cabeza y avanza hasta comerla."""
    if choose_fruit is not None:
        controller.game.chooseFruit = choose_fruit
    game.fruitPosX = game.head.rect.x + game.sizeSprite
    game.fruitPosY = game.head.rect.y
    game.existsFruit = True
    before = game.contFruit
    for _ in range(max_frames):
        play_frame(controller, pygame.K_RIGHT)
        if game.contFruit > before:
            return
    raise AssertionError("no se comió la fruta")


@pytest.fixture
def controller(view, monkeypatch):
    from controller.audio_controller import AudioController

    monkeypatch.setattr(AudioController, "repSound", lambda self, sound: None)
    monkeypatch.setattr(AudioController, "repMusic", lambda self, music: None)

    from controller.controller import Controller

    return Controller(view)


# --- Flujo del modo clásico ---


def test_escape_key_pauses_game(controller):
    game = start_classic(controller)

    post_keys(pygame.K_ESCAPE)
    controller.handleGameEvents()

    assert game.paused is True


def test_keyboard_input_moves_snake(controller):
    game = start_classic(controller)

    play_frame(controller, pygame.K_RIGHT)

    assert (game.head.rect.x, game.head.rect.y) == (START_HEAD_X + SPRITE_SIZE, START_HEAD_Y)


def test_snake_changes_direction_between_frames(controller):
    game = start_classic(controller)

    play_frame(controller, pygame.K_RIGHT)
    play_frame(controller, pygame.K_UP)

    assert game.speedX == 0
    assert game.speedY == -game.sizeSprite


def test_eating_fruit_updates_score_and_growth(controller):
    game = start_classic(controller)

    eat_fruit(controller, game)

    assert game.contFruit == 1
    assert len(game.parts) == 2
    assert game.score == SCORE_PER_FRUIT * game.speedGame
    assert game.existsFruit is True


def test_game_flow_ends_in_game_over(controller):
    game = start_classic(controller)

    for _ in range(40):
        play_frame(controller, pygame.K_RIGHT)
        if game.gameOver:
            break

    assert game.gameOver is True
    assert game.head.rect.x > BOARD_MAX_COL * game.sizeSprite


# --- Flujo del modo 2.0 (Adapter) ---


def test_adapter_reversed_controls_after_special_fruit(controller):
    adapter = start_adapter(controller)
    game = adapter.gameController
    random.seed(42)

    eat_fruit(controller, game, choose_fruit="fruit4")

    assert adapter.fruitType == 4

    play_frame(controller, pygame.K_UP)

    assert game.speedX == 0
    assert game.speedY == game.sizeSprite


def test_adapter_spawns_wall_every_two_fruits(controller):
    adapter = start_adapter(controller)
    game = adapter.gameController
    random.seed(7)

    eat_fruit(controller, game, choose_fruit="fruit1")
    eat_fruit(controller, game, choose_fruit="fruit1")

    assert game.contFruit == 2
    assert adapter.contWall == 1
    assert len(adapter.walls) == 1
