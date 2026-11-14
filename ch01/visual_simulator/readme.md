# 🧭 Simulador Visual de Algoritmos de Búsqueda en IA

Entorno interactivo desarrollado en **Python** y **Pygame** para visualizar, comparar y analizar el comportamiento de algoritmos de búsqueda informada y no informada sobre ambientes representados como laberintos con obstáculos y costos variables. Este entorno permite abstraer conceptos complejos tales como agente, espacio de estados, set de acciones, rutas óptimas, costo acumulado y número de nodos visitados, los cuales convencionalmente se describen mediante árboles de búsqueda o grafos. 

---

## 📑 Tabla de Contenidos
1. [Características Principales](#-características-principales)
2. [Instalación y Ejecución](#-instalación-y-ejecución)
3. [Fundamentos Teóricos de los Algoritmos](#-fundamentos-teóricos-de-los-algoritmos)
   - [Agente, Ambiente, Espacio de Estados y Set de Acciones](#agente)
   - [DFS (Búsqueda en Profundidad)](#dfs) 
   - [BFS (Búsqueda en Anchura)](#bfs)
   - [UCS (Búsqueda de Costo Uniforme)](#ucs)
   - [GBFS (Búsqueda Basada en Heurísticas)](#gbfs)
   - [A* (A-Estrella)](#a-star)
4. [Guía de Laboratorio: Experimentos Sugeridos](#-guía-de-laboratorio-experimentos-sugeridos)

---

## ✨ Características Principales
* **6 Estrategias de Búsqueda:** DFS, BFS, UCS, GBFS (Heurística Euclidiana), GBFS (Heurística Manhattan) y A*.
* **Dos Escenarios de Prueba:** Un laberinto simple para comprensión básica y un laberinto complejo con puentes, ríos de lava y abismos.
* **Manipulación del Entorno en Vivo:** Cambio dinámico del nodo inicial y edición personalizada de los costos de transición entre nodos.
* **Panel de Estadísticas:** Comparativa de nodos expandidos, costo total de la ruta y tiempo de ejecución[cite: 6, 13].

---

## 🚀 Instalación y Ejecución

### Requisitos previos
* Python 3.8 o superior.

### Pasos
1. Clona este repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
   cd tu-repositorio

---
## 🧠 Fundamentos Teóricos de los Algoritmos
Los algoritmos de búsqueda son pilares fundamentales de la inteligencia artificial y han sido ampliamente utilizados para resolver problemas en los que a partir de un estado inicial se requiere llegar a un estado meta. Dentro de las aplicaciones de estos algoritmos se pueden encontrar soluciones para planificación de rutas y navegación geográfica (Google Maps), navegación en vehículos autónomos, pathfinding en video juegos, optimización de rutas en cadenas de suministro y enrutamiento de paquetes en redes de comunicaciones, entre muchas otras más.

### Agente
Un agente representa a una entidad con capacidad computacional que advierte los cambios en el ambiente mediante sensores y actúa de acuerdo con el conjunto de acciones disponible, hasta alcanzar el objetivo. Un agente puede representar a múltiples entidades dentro del contexto de la inteligencia artificial. Puede ser un vehículo autónomo, el cual puede decidir sobre sus acciones dependiendo de las variaciones del tráfico; un generador fotovoltaico o eólico que toma decisiones de acuerdo a los niveles de energía disponible en las baterías, la radiación solar o intensidad de los vientos y la demanda de energía; un vehículo aéreo no tripulado usado para agricultura de precisión en riego o fumigación de cultivos que decide sobre los niveles de agua o pesticida que debe aplicar dependiendo de la resequedad de la planta o nivel de plaga, respectivamente; un dron usado para actividades de búsqueda y rescate que identifica posibles víctimas a través de objetos tales como ropa, zapatos u otros elementos que sugieren la presencia de personas; un software de asistencia personal que agenda citas o automatiza actividades recurrentes.
Recuerde que un agente opera dentro de un ambiente, y que ese ambiente posee múltiples estados que conforman lo que conocemos como espacio de estados. Dentro de cada estado, el agente puede tomar decisiones, es decir, ejecutar acciones que pertenecen al set de acciones. Esto se ilustra mejor en la Figura 1.

<img width="300" height="300" alt="R4_1" align='center' src="https://github.com/user-attachments/assets/ed1631b6-b3e6-4580-899c-f7f9ef371420" />


### DFS (Búsqueda en Profundidad)

