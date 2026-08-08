# SnakeGame

[![CI](https://github.com/JuanSotelo9/SnakeGame/actions/workflows/ci.yml/badge.svg)](https://github.com/JuanSotelo9/SnakeGame/actions/workflows/ci.yml)

Juego de la serpiente (Snake) implementado en Python usando Pygame.

Este proyecto usa el patrón Adapter para añadir un modo alternativo de juego
manteniendo la versión clásica como referencia. Hay dos modos principales:

- **Modo clásico:** Implementación tradicional del juego Snake.
- **Modo 2.0:** Variante con muros, cuatro tipos de fruta con probabilidades
  distintas y controles invertidos al comer la fruta especial. Reutiliza la
  infraestructura del modo clásico a través de un adaptador.

La arquitectura sigue el patrón **MVC** (Modelo-Vista-Controlador), separando
claramente la lógica del juego, el renderizado y el manejo de eventos.

**Estado:** Proyecto local

## Requisitos

- Python 3.10 o superior
- Pygame (>= 2.0)

## Instalación

1. Clona o descarga este repositorio.
2. Crea y activa un entorno virtual (recomendado):

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecutar el juego

Desde la raíz del proyecto:

```bash
cd src/snake
python -m controller.main
```

## Pruebas y linting

La lógica del juego está cubierta por una suite de pytest y el estilo se valida
con ruff. Instala las dependencias de desarrollo y ejecuta ambas desde la raíz
del proyecto:

```bash
pip install -r requirements-dev.txt

pytest                 # ejecuta los tests
ruff check src tests   # lint
ruff format --check src tests   # verifica el formato
```

Los tests usan los drivers `dummy` de SDL, por lo que se ejecutan sin necesidad
de pantalla ni audio. La suite incluye tests unitarios (lógica de `GameController`
y botones) y tests de integración que simulan inputs del teclado con
`pygame.event.post` y verifican el estado del juego a lo largo del bucle de juego.
El CI (GitHub Actions) corre estos pasos en cada push.

## Estructura del proyecto

```
src/snake/
├── assets/
│   ├── images/        # Sprites y fondos
│   └── sounds/        # Música y efectos de sonido
├── controller/        # Lógica del juego y manejo de eventos
│   ├── main.py        # Punto de entrada
│   ├── controller.py  # Orquestación de pantallas y menús
│   ├── game_controller.py              # Modo clásico
│   └── game_controller_adapter.py      # Modo 2.0 (patrón Adapter)
├── model/             # Clases del modelo: body, fruit, wall, button
├── view/              # Renderizado con Pygame (view.py)
├── data/              # Datos de guardado y puntajes (generados en ejecución)
├── config.py          # Constantes y parámetros centralizados del juego
└── paths.py           # Rutas absolutas a assets y datos
tests/                 # Suite de pruebas con pytest
.github/workflows/     # CI: lint + tests en cada push
pyproject.toml         # Configuración de pytest y ruff
```

Los archivos de guardado (`.pkl`) se generan en ejecución dentro de `data/` y
están excluidos del control de versiones.
