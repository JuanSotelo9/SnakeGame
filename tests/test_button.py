from model.button import Button
from paths import image_path


def make_button(x=100, y=148, weight=255, height=69):
    return Button(x, y, image_path("btn_play1.png"), weight, height)


def test_is_clicked_inside_bounds():
    button = make_button()

    assert button.is_clicked((100, 148)) is True
    assert button.is_clicked((354, 216)) is True


def test_is_clicked_outside_bounds():
    button = make_button()

    assert button.is_clicked((99, 148)) is False
    assert button.is_clicked((100, 147)) is False
    assert button.is_clicked((355, 148)) is False


def test_is_clicked_respects_button_geometry():
    button = make_button(x=50, y=200, weight=100, height=40)

    assert button.is_clicked((149, 239)) is True
    assert button.is_clicked((150, 240)) is False


def test_rect_matches_creation_position():
    button = make_button(x=33, y=375, weight=187, height=69)

    assert (button.rect.x, button.rect.y) == (33, 375)
    assert (button.rect.width, button.rect.height) == (187, 69)
