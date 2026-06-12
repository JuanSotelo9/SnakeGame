import pygame, sys, os

# Obtener la ruta del directorio raíz del proyecto (Snake)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Agregar la ruta del directorio raíz al principio de sys.path
sys.path.insert(0, project_root)

from view.view import View
from Controller import Controller

# Función principal del programa
if __name__ == "__main__":

    # Inicialización Programa
    pygame.init()
    view = View()
    controller = Controller(view)

    controller.handleMenuEvents()
