# SnakeGame

Juego de la serpiente (Snake) implementado en Python usando Pygame.
Este proyecto usa el patrón Adapter para añadir un modo alternativo de juego
manteniendo la versión clásica como referencia. Hay dos modos principales:

- Modo clásico: Implementación tradicional del juego Snake.
- Modo con Adapter: Se introduce un adaptador que crea otro modo de juego
	(por ejemplo, una variante con distinta lógica de movimiento o entrada)
	reutilizando la mayor parte de la infraestructura existente.

Se separan claramente las capas de controlador, modelo y vista.

**Estado:** Proyecto local

## Requisitos
- Python 3.10 o superior
- Pygame (recomendado >= 2.0)

Si usas Windows, instala Python desde https://www.python.org/ y asegúrate de
añadir Python al PATH.

## Instalación (rápida)

1. Clona o descarga este repositorio.
2. Crea y activa un entorno virtual (recomendado):

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instala dependencias:

```bash
pip install pygame
```

## Ejecutar el juego

Desde la raíz del proyecto, ejecuta:

```bash
python src\Snake\controller\main.py
```

El punto de entrada principal está en `src/Snake/controller/main.py`.

## Estructura del proyecto

Breve vista de las carpetas y archivos principales:

- `src/Snake/controller/` — Controladores y punto de entrada (`main.py`).
- `src/Snake/view/` — Lógica de renderizado basada en Pygame (`view.py`).
- `src/Snake/model/` — Clases del modelo: `Body.py`, `Fruit.py`, `Wall.py`, `Button.py`.
- `src/Snake/images/` — Recursos de imágenes usados por la vista.
- `src/Snake/sounds/` — Archivos de audio (se reproducen con `pygame.mixer`).

Explora `src/Snake/controller/Controller.py` y `src/Snake/view/view.py` para ver
cómo se coordinan la entrada, la lógica del juego y el render.

