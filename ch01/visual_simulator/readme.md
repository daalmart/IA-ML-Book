# 🧭 Simulador Visual de Algoritmos de Búsqueda en IA

Entorno interactivo desarrollado en **Python** y **Pygame** para visualizar, comparar y analizar el comportamiento de algoritmos de búsqueda informada y no informada sobre grafos representados como laberintos con obstáculos y costos variables[cite: 1, 13].

---

## 📑 Tabla de Contenidos
1. [Características Principales](#-características-principales)
2. [Instalación y Ejecución](#-instalación-y-ejecución)
3. [Guía de Controles e Interfaz](#-guía-de-controles-e-interfaz)
4. [Fundamentos Teóricos de los Algoritmos](#-fundamentos-teóricos-de-los-algoritmos)
   - [DFS (Búsqueda en Profundidad)](#dfs)
   - [BFS (Búsqueda en Anchura)](#bfs)
   - [UCS (Búsqueda de Costo Uniforme)](#ucs)
   - [GBFS (Búsqueda Voraz Primero el Mejor)](#gbfs)
   - [A* (A-Estrella)](#a-star)
5. [Guía de Laboratorio: Experimentos Sugeridos](#-guía-de-laboratorio-experimentos-sugeridos)

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
## :mortar_board: Fundamentos Teóricos de los Algoritmos
Los algoritmos de búsqueda son pilares fundamentales de la inteligencia artificial y han sido ampliamente utilizados para resolver problemas en los que a partir de un estado inicial se requiere llegar a un estado meta. Dentro de las aplicaciones de estos algoritmos se pueden encontrar soluciones para planificación de rutas y navegación geográfica (Google Maps), navegación en vehículos autónomos, pathfinding en video juegos, optimización de rutas en cadenas de suministro y enrutamiento de paquetes en redes de comunicaciones, entre muchas otras más.
### DFS (Búsqueda en Profundidad)
