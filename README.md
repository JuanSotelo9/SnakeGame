# Snake Game

[![CI](https://github.com/JuanSotelo9/SnakeGame/actions/workflows/ci.yml/badge.svg)](https://github.com/JuanSotelo9/SnakeGame/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-58A616.svg)](https://www.pygame.org/)


Juego de la serpiente (Snake) desarrollado en **Python** con **Pygame**, construido
sobre una arquitectura **Modelo-Vista-Controlador (MVC)** y extendido con el patrón
**Adapter** para añadir un segundo modo de juego reutilizando la lógica del primero.

Es un proyecto orientado a buenas prácticas: cobertura de pruebas unitarias y de
integración, linting con `ruff`, integración continua con GitHub Actions y
contenedor Docker para ejecutarlo sin instalar Python.

## Contenido

- [Características](#características)
- [Modos de juego](#modos-de-juego)
- [Arquitectura](#arquitectura)
- [Stack tecnológico](#stack-tecnológico)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Empezar](#empezar)
- [Pruebas y calidad](#pruebas-y-calidad)
- [Integración continua](#integración-continua)
- [Mejoras futuras](#mejoras-futuras)
- [Autor](#autor)

## Características

- Dos modos de juego: clásico y extendido (patrón Adapter).
- Menú con puntajes, créditos y guardado/carga de partidas.
- Audio y música de fondo con `pygame.mixer`.
- Controles por teclado (flechas / WASD) y pausa con `ESC`.
- Tabla de puntajes persistente (top 5).

## Modos de juego

**Modo clásico**

El snake crece al comer frutas, la velocidad aumenta cada 15 frutas y la partida
termina al chocar con las paredes o con el propio cuerpo.

**Modo 2.0 (Adapter)**

Extiende el modo clásico reutilizando su infraestructura:

- Aparecen muros cada 2 frutas que la cabeza no puede atravesar.
- Cuatro tipos de fruta con probabilidades distintas:

  | Fruta | Probabilidad | Efecto |
  |---|---|---|
  | Fruta 1 | 75% | Normal |
  | Fruta 2 | 15% | Puntuación extra |
  | Fruta 3 | 1% | Destruye muros |
  | Fruta 4 | 9% | Invierte los controles |

## Arquitectura

El proyecto separa claramente la lógica de juego, el renderizado y el manejo de
eventos siguiendo el patrón **MVC**, y aplica el patrón **Adapter** para el modo 2.0.

```
┌───────────────┐      ┌───────────────────┐
│     View      │      │    Controller     │
│ (renderizado) │◄────►│ (eventos y menús) │
└───────────────┘      └─────────┬─────────┘
                                 │
                   ┌─────────────┴─────────────┐
                   │      GameController       │
                   │       (modo clásico)      │
                   └─────────────┬─────────────┘
                                 │
                   ┌─────────────┴─────────────┐
                   │  GameControllerAdapter    │
                   │        (modo 2.0)         │
                   └─────────────┬─────────────┘
                                 │
                   ┌─────────────┴─────────────┐
                   │      Model (sprites)      │
                   └───────────────────────────┘
```

Decisiones de diseño relevantes:

- `GameControllerInterface` es una **clase abstracta** (`abc.ABC`) que define el
  contrato de la lógica de juego.
- El **Adapter** envuelve al `GameController` y le agrega muros, frutas especiales
  y controles invertidos sin duplicar la lógica base.
- Los botones exponen su propia detección de clic (`is_clicked`), delegando en su
  propio `rect`.
- Las imágenes estáticas se cargan **una sola vez** en la vista, no por frame.
- Los parámetros del juego (tamaño de sprites, velocidades, colores, layouts de
  botones) están centralizados en `config.py`.

## Stack tecnológico

| Tecnología | Uso |
|---|---|
| Python 3.10+ | Lenguaje principal |
| Pygame | Renderizado, eventos y audio |
| pytest | Tests unitarios y de integración |
| ruff | Linting y formato |
| GitHub Actions | Integración continua |

## Estructura del proyecto

```
src/snake/
├── assets/
│   ├── images/                    # Sprites y fondos
│   └── sounds/                    # Música y efectos de sonido
├── controller/
│   ├── main.py                    # Punto de entrada
│   ├── controller.py              # Orquestación de pantallas y menús
│   ├── game_controller.py         # Lógica del modo clásico
│   ├── game_controller_adapter.py # Modo 2.0 (patrón Adapter)
│   └── audio_controller.py        # Música y efectos de sonido
├── model/                         # Clases del modelo: body, fruit, wall, button
├── view/                          # Renderizado con Pygame
├── data/                          # Guardado de partidas y puntajes (generados)
├── config.py                      # Constantes y parámetros centralizados
└── paths.py                       # Rutas absolutas a assets y datos
tests/                             # Suite de pruebas (unitarias e integración)
.github/workflows/                 # CI: lint + tests en cada push
```

## Empezar

### Requisitos

- Python 3.10 o superior
- Pygame >= 2.0

### Instalación

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
```

### Ejecución

```bash
cd src/snake
python -m controller.main
```

## Pruebas y calidad

La suite incluye **31 tests**: unitarios para la lógica de `GameController` y los
botones, y de integración que simulan inputs del teclado con `pygame.event.post`
verificando el estado del juego a lo largo del bucle de juego.

```bash
pip install -r requirements-dev.txt

pytest                       # ejecuta la suite completa
ruff check src tests         # linting
ruff format --check src tests   # verifica el formato
```

Los tests usan los drivers `dummy` de SDL, por lo que se ejecutan sin necesidad
de pantalla ni audio.

## Integración continua

GitHub Actions corre en cada push:

- `ruff check` y `ruff format --check` sobre `src` y `tests`.
- `pytest` en una matriz de Python 3.10, 3.11 y 3.12.

## Mejoras futuras

- Reemplazar `pickle` por un formato más robusto (por ejemplo, JSON) para el
  guardado de partidas y puntajes.
- Añadir ajustes de volumen y dificultad en la pausa.
- Modo online con tabla de puntajes global (API + frontend).
- Empaquetar como ejecutable con PyInstaller y publicar releases.

## Autor

Proyecto universitario. Repositorio: [JuanSotelo9](https://github.com/JuanSotelo9).
