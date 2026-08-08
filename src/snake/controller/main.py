import pygame
from controller.controller import Controller
from view.view import View


def main() -> None:
    pygame.init()
    try:
        view = View()
    except pygame.error as error:
        print("No se pudo abrir la ventana del juego.")
        print("Revisa que tengas una pantalla disponible (variable DISPLAY) y que")
        print("el socket de X11 esté montado si ejecutas dentro de Docker.")
        print(f"Detalle del error: {error}")
        pygame.quit()
        return
    controller = Controller(view)
    controller.handleMenuEvents()


if __name__ == "__main__":
    main()
