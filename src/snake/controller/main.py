import pygame
from controller.controller import Controller
from view.view import View


def main() -> None:
    pygame.init()
    view = View()
    controller = Controller(view)
    controller.handleMenuEvents()


if __name__ == "__main__":
    main()
