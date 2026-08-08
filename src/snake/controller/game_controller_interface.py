from abc import ABC, abstractmethod


class GameControllerInterface(ABC):
    """Contrato que deben implementar los controladores de juego."""

    @abstractmethod
    def newGame(self) -> None:
        """Inicia una partida nueva."""
        ...

    @abstractmethod
    def startGame(self) -> None:
        """Ejecuta un frame de la lógica del juego."""
        ...

    @abstractmethod
    def setSpeeds(self, event) -> None:
        """Actualiza la dirección del snake según el evento de teclado."""
        ...

    @abstractmethod
    def addBody(self) -> None:
        """Agrega una parte al cuerpo del snake."""
        ...

    @abstractmethod
    def createFruit(self, type):
        """Crea una fruta en una posición disponible."""
        ...

    @abstractmethod
    def itsAvailable(self, x, y) -> bool:
        """Comprueba si la posición (x, y) está libre."""
        ...

    @abstractmethod
    def moveSnake(self) -> None:
        """Mueve todas las partes del snake."""
        ...

    @abstractmethod
    def itsGameOver(self) -> bool:
        """Comprueba si se produjo un game over."""
        ...

    @abstractmethod
    def saveGame(self) -> None:
        """Guarda el estado actual de la partida."""
        ...

    @abstractmethod
    def loadGame(self) -> None:
        """Carga el estado guardado de la partida."""
        ...
