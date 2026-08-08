import pygame
import pytest
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
from paths import image_path


def key_event(key):
    return pygame.event.Event(pygame.KEYDOWN, key=key)


def test_new_game_resets_state(game_controller):
    gc = game_controller
    gc.newGame()

    assert gc.score == 0
    assert gc.speedGame == INITIAL_SPEED
    assert gc.speedX == 0
    assert gc.speedY == 0
    assert gc.gameOver is False
    assert gc.paused is False
    assert len(gc.parts) == 1
    assert (gc.head.rect.x, gc.head.rect.y) == (START_HEAD_X, START_HEAD_Y)


@pytest.mark.parametrize(
    "key,expected_x,expected_y",
    [
        (pygame.K_RIGHT, SPRITE_SIZE, 0),
        (pygame.K_LEFT, -SPRITE_SIZE, 0),
        (pygame.K_UP, 0, -SPRITE_SIZE),
        (pygame.K_DOWN, 0, SPRITE_SIZE),
    ],
)
def test_set_speeds_sets_direction(game_controller, key, expected_x, expected_y):
    gc = game_controller
    gc.newGame()
    gc.setSpeeds(key_event(key))

    assert gc.speedX == expected_x
    assert gc.speedY == expected_y
    assert gc.key is True


def test_cannot_reverse_direction_into_itself(game_controller):
    gc = game_controller
    gc.newGame()
    gc.speedX = SPRITE_SIZE

    gc.setSpeeds(key_event(pygame.K_LEFT))

    assert gc.speedX == SPRITE_SIZE
    assert gc.speedY == 0


def test_move_snake_moves_head(game_controller):
    gc = game_controller
    gc.newGame()
    start_x, start_y = gc.head.rect.x, gc.head.rect.y

    gc.setSpeeds(key_event(pygame.K_RIGHT))
    gc.moveSnake()

    assert (gc.head.rect.x, gc.head.rect.y) == (start_x + SPRITE_SIZE, start_y)


def test_snake_body_follows_head(game_controller):
    gc = game_controller
    gc.newGame()
    gc.setSpeeds(key_event(pygame.K_RIGHT))
    gc.moveSnake()
    gc.addBody()
    gc.moveSnake()
    gc.addBody()
    for _ in range(3):
        gc.moveSnake()

    assert gc.head.rect.x == gc.parts[1].rect.x + SPRITE_SIZE
    assert gc.parts[1].rect.x == gc.parts[2].rect.x + SPRITE_SIZE
    assert gc.head.rect.y == gc.parts[1].rect.y == gc.parts[2].rect.y


def test_eating_fruit_increases_score_and_grows(game_controller):
    gc = game_controller
    gc.newGame()
    gc.fruitPosX, gc.fruitPosY = gc.head.rect.x, gc.head.rect.y
    gc.existsFruit = True

    gc.startGame()

    assert gc.score == SCORE_PER_FRUIT * gc.speedGame
    assert gc.contFruit == 1
    assert len(gc.parts) == 2
    assert gc.existsFruit is True


def test_no_score_or_growth_without_eating(game_controller):
    gc = game_controller
    gc.newGame()

    gc.startGame()

    assert gc.score == 0
    assert gc.contFruit == 0
    assert len(gc.parts) == 1


def test_speed_increases_every_speed_up_every_fruits(game_controller):
    gc = game_controller
    gc.newGame()
    for _ in range(SPEED_UP_EVERY):
        gc.addBody()

    assert gc.speedGame == INITIAL_SPEED + 1


def test_speed_caps_at_max(game_controller):
    gc = game_controller
    gc.newGame()
    gc.speedGame = MAX_SPEED
    gc.contFruit = SPEED_UP_EVERY - 1

    gc.addBody()

    assert gc.speedGame == MAX_SPEED


def test_wall_collision_is_game_over(game_controller):
    gc = game_controller
    gc.newGame()

    gc.head.rect.x = BOARD_MAX_COL * SPRITE_SIZE + 1
    assert gc.itsGameOver() is True

    gc.head.rect.x = START_HEAD_X
    gc.head.rect.y = BOARD_MIN_ROW * SPRITE_SIZE - 1
    assert gc.itsGameOver() is True


def test_inside_board_is_not_game_over(game_controller):
    gc = game_controller
    gc.newGame()

    assert gc.itsGameOver() is False


def test_self_collision_is_game_over(game_controller):
    gc = game_controller
    gc.newGame()
    gc.addBody()
    gc.parts[1].rect.x, gc.parts[1].rect.y = gc.head.rect.x, gc.head.rect.y

    assert gc.itsGameOver() is True


def test_fruit_spawns_within_board(game_controller):
    gc = game_controller
    gc.newGame()

    for _ in range(100):
        fruit = gc.createFruit(image_path("fruit1.png"))
        assert BOARD_MIN_COL * gc.sizeSprite <= fruit.rect.x <= BOARD_MAX_COL * gc.sizeSprite
        assert BOARD_MIN_ROW * gc.sizeSprite <= fruit.rect.y <= BOARD_MAX_ROW * gc.sizeSprite


def test_fruit_never_spawns_on_snake(game_controller):
    gc = game_controller
    gc.newGame()
    for _ in range(10):
        gc.addBody()

    for _ in range(50):
        fruit = gc.createFruit(image_path("fruit1.png"))
        for part in gc.parts:
            assert (fruit.rect.x, fruit.rect.y) != (part.rect.x, part.rect.y)


def test_its_available_detects_occupied_cells(game_controller):
    gc = game_controller
    gc.newGame()
    x, y = gc.head.rect.x, gc.head.rect.y

    assert gc.itsAvailable(x, y) is False
    assert gc.itsAvailable(x + SPRITE_SIZE, y) is True


def test_save_load_roundtrip(game_controller, tmp_path, monkeypatch):
    monkeypatch.setattr("paths.DATA_DIR", tmp_path)
    gc = game_controller
    gc.newGame()
    gc.addBody()
    gc.addBody()
    gc.score = 42
    gc.speedGame = 7
    gc.fruitPosX, gc.fruitPosY = 200, 140

    gc.saveGame()
    gc.newGame()
    gc.loadGame()

    assert gc.score == 42
    assert gc.speedGame == 7
    assert (gc.fruitPosX, gc.fruitPosY) == (200, 140)
    assert len(gc.parts) == 3


def test_load_missing_save_starts_new_game(game_controller, tmp_path, monkeypatch):
    monkeypatch.setattr("paths.DATA_DIR", tmp_path)
    gc = game_controller
    gc.newGame()
    gc.score = 999

    gc.loadGame()

    assert gc.score == 0
    assert gc.gameOver is False
    assert len(gc.parts) == 1
