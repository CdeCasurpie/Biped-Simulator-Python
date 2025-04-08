# Biped-Simulator-Python

Un simulador físico de bípedos en Python con animaciones procedurales para caminar, utilizando pygame para la representación gráfica.

![image](https://github.com/user-attachments/assets/b4c32017-90a9-4bc8-9be6-dbad93491b6d)

## Descripción

Este proyecto implementa un motor de física simple para simular el movimiento de un bípedo (entidad de dos piernas) con cinemática inversa. El sistema utiliza resortes, puntos físicos y restricciones para crear un movimiento natural y realista.

Características principales:
- Sistema de física basado en puntos y resortes
- Cinemática inversa para el cálculo de las articulaciones
- Detección y respuesta a colisiones
- Animación procedural de caminata
- Control interactivo del bípedo

## Requisitos

- Python 3.6+
- Pygame

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tuusuario/Biped-Simulator-Python.git
cd Biped-Simulator-Python
```

2. Instala las dependencias:
```bash
pip install pygame
```

## Uso

Para ejecutar la simulación:

```bash
python main.py
```

### Controles

- **Flechas izquierda/derecha**: Mover el bípedo horizontalmente
- **Flechas arriba/abajo**: Mover el bípedo verticalmente
- **Tecla U**: Aumentar velocidad
- **Tecla Y**: Disminuir velocidad

## Arquitectura del Proyecto

El proyecto está organizado en módulos para facilitar su mantenimiento:

- `simulation/core.py`: Clases fundamentales para la física (Point, Line, PhysicalPoint, RectangleCollider)
- `simulation/spring.py`: Implementación de la restricción de resorte
- `simulation/biped.py`: Lógica específica del bípedo, incluyendo cinemática inversa
- `simulation/engine.py`: Motor de simulación general
- `simulation/config.py`: Parámetros de configuración global
- `main.py`: Punto de entrada que configura e inicia la simulación

### Componentes Principales

#### Puntos Físicos (PhysicalPoint)
Representan objetos que responden a fuerzas físicas, tienen masa, velocidad y aceleración.

#### Restricciones de Resorte (SpringConstraint)
Conectan dos puntos y aplican fuerzas para mantener una distancia específica entre ellos, simulando un resorte con rigidez y amortiguación.

#### Cinemática Inversa
El método `inverse_kinematics` en la clase `Biped` calcula la posición de las articulaciones (rodillas) basado en la posición de la cadera y los pies.

#### Sistema de Colisiones
Detección y respuesta a colisiones entre puntos físicos y colisionadores rectangulares.

## Funcionamiento del Bípedo

El bípedo está compuesto por:
- Un punto principal (main_point) que representa el centro de control
- Una cadera (hip) que es un punto físico conectado al punto principal mediante un resorte
- Dos pies (foot_left, foot_right) que se mueven para mantener el equilibrio
- Dos muslos (thigh_left, thigh_right) calculados mediante cinemática inversa

El movimiento sigue estos principios:
1. El punto principal se mueve según la entrada del usuario
2. La cadera sigue al punto principal mediante la fuerza del resorte
3. Los pies se mueven para mantener el centro de gravedad entre ellos
4. La altura del paso y la distancia entre piernas se ajustan según la velocidad
5. La cinemática inversa calcula la posición de las rodillas

## Personalización

Puedes ajustar diversos parámetros en `simulation/config.py`:
- `GRAVITY`: Fuerza de gravedad
- `AMORTIGUACION`: Factor de amortiguación del movimiento
- `WIDTH`, `HEIGHT`: Dimensiones de la ventana

En la clase `Biped` también puedes modificar:
- `speed`: Velocidad de movimiento
- `step_height`: Altura máxima del paso
- `thigh_length`: Longitud del muslo
- `calf_length`: Longitud de la pantorrilla

## Ampliación del Proyecto

Algunas ideas para ampliar el proyecto:
- Añadir más articulaciones para un movimiento más complejo
- Implementar detección de colisiones con el entorno
- Crear diferentes tipos de terreno
- Añadir un sistema de aprendizaje para optimizar el movimiento


## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios importantes antes de enviar un pull request.

---

*Proyecto desarrollado por César Perales y Melisa Rivera*
