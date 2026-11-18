# 🧭 Simulador Visual de Algoritmos de Búsqueda en IA

Entorno interactivo desarrollado en **Python** y **Pygame** para visualizar, comparar y analizar el comportamiento de algoritmos de búsqueda informada y no informada sobre ambientes representados como laberintos con obstáculos y costos variables. Este entorno permite abstraer conceptos complejos tales como agente, espacio de estados, set de acciones, rutas óptimas, costo acumulado y número de nodos visitados, los cuales convencionalmente se describen mediante árboles de búsqueda o grafos. 

---

## 📑 Tabla de Contenidos
1. [Características Principales](#-características-principales)
2. [Instalación y Ejecución](#-instalación-y-ejecución)
3. [Fundamentos Teóricos de los Algoritmos](#-fundamentos-teóricos-de-los-algoritmos)
   - [Agente](#agente)
   - [Árbol de Búsqueda](#árbol-de-búsqueda)
   - [Depth First Search](#depth-first-search) 
   - [Breadth First Search](#breadth-first-search)
   - [Uniform Cost Search](#uniform-cost-search)
   - [Greedy Best First Search](#gbfs)
   - [A*](#a)
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
Los algoritmos de búsqueda son pilares fundamentales de la inteligencia artificial y han sido ampliamente utilizados para resolver problemas en los que a partir de un estado inicial se requiere llegar a un estado meta. Dentro de las aplicaciones de estos algoritmos se pueden encontrar soluciones para planificación de rutas y navegación geográfica (Google Maps), navegación en vehículos autónomos, pathfinding en video juegos, optimización de rutas en cadenas de suministro y enrutamiento de paquetes en redes de comunicaciones, entre muchas otras más. A continuación se describen los principales conceptos relacionados con los algoritmos de búsqueda informada y no informada, con el fin de dar soporte al simulador desarrollado. Para obtener información más detallada, se puede dirigir al libro del curso de introducción a la inteligencia artificial, disponible en: <a href="https://github.com/daalmart/IA-ML-Book/blob/main/ch01/ch01.pdf">Capítulo 1.</a>

---
### Agente
Un agente representa a una entidad con capacidad computacional que advierte los cambios en el ambiente mediante sensores y actúa de acuerdo con el conjunto de acciones disponible, hasta alcanzar el objetivo. Un agente puede representar a múltiples entidades dentro del contexto de la inteligencia artificial. Puede ser un vehículo autónomo, el cual puede decidir sobre sus acciones dependiendo de las variaciones del tráfico; un generador fotovoltaico o eólico que toma decisiones de acuerdo a los niveles de energía disponible en las baterías, la radiación solar o intensidad de los vientos y la demanda de energía; un vehículo aéreo no tripulado usado para agricultura de precisión en riego o fumigación de cultivos que decide sobre los niveles de agua o pesticida que debe aplicar dependiendo de la resequedad de la planta o nivel de plaga, respectivamente; un dron usado para actividades de búsqueda y rescate que identifica posibles víctimas a través de objetos tales como ropa, zapatos u otros elementos que sugieren la presencia de personas; un software de asistencia personal que agenda citas o automatiza actividades recurrentes.
Un agente opera dentro de un ambiente, y que ese ambiente posee múltiples estados que conforman lo que conocemos como espacio de estados. Dentro de cada estado, el agente puede tomar decisiones, es decir, ejecutar acciones que pertenecen al set de acciones. Esto se ilustra mejor en la Figura 1.

<p align="center">
  <img width="300" height="300" alt="R4_1" src="../resources/figures/R4_1.png" />
  <br>
  <em>Figura 1: Un agente (vehículo) dentro de un ambiente con un espacio de estados y un set de acciones (arriba, abajo, derecha e izquierda). En este caso, el espacio de estados está dado por posiciones que el vehículo puede ocupar en su ruta desde el estado inicial hacia el el estado meta (bandera verde).</em>
</p>
Un agente puede calcular el conjunto de estados por los que debe pasar para llegar a la meta bajo diferentes condiciones que inluyen transiciones entre estados a través de acciones, costos de las acciones, valores de heurística y combinaciones de estos dos últimos parámetros. Para ello utiliza algoritmos de búsqueda informada y no informada. La búsqueda no informada involucra el conocimiento del estado inicial y el estado meta, junto con costos de las acciones. Dentro de estos algoritmos tenemos DFS (Depth First Search), BFS (Breadth First Search) y UCS (Uniform Cost Search) también denominado Dijkstra en honor al matemático y científico de la computación neerlandés Edsger W. Dijkstra. Por otra parte, los algoritmos de búsqueda informada usan valores de heurística para proporcionar cierta información sobre la ruta que el agente debe seguir con el fin de llegar a la meta con un costo menor. Dentro de este tipo de algoritmos tenemos GBFS (Greedy Best First Search) y A*, el primero basado completamente en heurísticas, y el segundo basado en la combinación de estos valores y el costo entre acciones. En el caso del simulador mostrado en esta sección, los valores de heurística siguen dos aproximaciones sobre los que el usuario puede escoger. La primera es una heurística Euclideana calculada desde cada estado hasta el estado meta usando la siguiente expresión:

$$h_{\text{euclidiana}}(n) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}.$$

La segunda se calcula también desde cada estado hasta el estado meta usando una distancia Mahnattan por medio de la siguiente expresión:

$$h_{\text{manhattan}}(n) = |x_1 - x_2| + |y_1 - y_2|,$$

donde $x_i$, $y_i$ representan las posiciones en el plano 2D para el agente mostrado en la Figura 1.

---
### Árbol de Búsqueda
Un árbol de búsqueda es un mecanismo gráfico que permite representar al espacio de estados mediante nodos (círculos) y las transiciones entre estos (enlaces entre nodos) que se producen por las acciones. En algunos casos, los enlaces entre nodos pueden incluir valores que reflejan los costos o recompensas por pasar de un estado a otro. En la Figura 2a, se muestra un ambiente en el que un agente tiene tres posibles rutas que parten de un estado inicial descrito por el círculo número uno. Cada círculo representa un estado del espacio de estados y puede interpretarse como una ubicación en un plano 2D con coordenadas (x,y). El agente puede moverse hacia los estados ejecutando las acciones representadas por las flechas. Es decir, tiene el siguiente set de acciones {adelante, atrás, izquierda y derecha}, pero algunas de estas no están disponibles en ciertos estados. La Figura 2b muestra la representación de este escenario a través de un árbol de búsqueda con un estado inicial o raíz dado por el círculo 1, un estado final o meta dado por el círculo 5, estados intermedios y acciones, las cuales son representadas como enlaces que conectan a los nodos para indicar las transiciones posibles entre estos. Algunos estados pueden aparecer más de una vez cuando hay varias transiciones que conducen a ellos, tal como ocurre con el estado meta y el estado 8. Es importante resaltar que generalmente en un árbol de búsqueda los enlaces no se simbolizan como flechas, lo cual indica que hay bi-direccionalidad entre estados. Esto significa que, dependiendo del problema, devolvernos de un estado X a un estado Y pueda requerir una acción no necesariamente contraria a la que produjo la transición entre Y y X.

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img width="300" alt="Escenario real." src="../resources/figures/searchTree.png" />
        <br />
        <sub><b>a) Escenario real.</b> Un agente con tres rutas diferentes. Algunas lo pueden llevar hasta la meta pero otras pueden ser fatales. El agente puede moverse a través de las ubicaciones dentro del laberinto, las cuales están representadas por círculos numerados. En este caso, tales ubicaciones representan los estados. La dirección de las flechas indica la acción que el agente puede usar en cada estado.</sub>
      </td>
      <td align="center">
        <img width="300" alt="Árbol de búsqueda." src="../resources/figures/search_tree_tikz.png" />
        <br />
        <sub><b>b) Árbol de búsqueda.</b> Algunos estados pueden aparecer más de una vez debido a que secuencias diferentes pueden conducir a ellos. En este caso tenemos dos rutas hacia el estado meta (Goal) y dos rutas diferentes para llegar al abismo con lava (estado 8).</sub>
      </td>
    </tr>
  </table>
  <p><em>Figura 2: Ejemplo de ambiente para un agente o vehículo autónomo (a), y su representación como un árbol de búsqueda (b).</em></p>
</div>

### Depth First Search
Es un algoritmo que hace una revisión de nodos hacia lo profundo de las ramas del árbol de búsqueda. Utiliza como mecanismo una pila tipo LIFO, en la cual inserta los nodos que se evalúan para identificar si son o no el nodo meta. Adicionalmente, cada nodo que ingresa a la pila  se marca como visitado para evitar ciclos infinitos. Cuando el nodo evaluado no es el nodo meta, se insertan en la pila sus nodos hijos y se repite el proceso hasta llegar a la solución. Si un nodo no tiene hijos, y además no es el nodo meta, el algoritmo genera un proceso de retroceso (backtracking) para seguir la búsqueda en el siguiente nodo disponible. Para entender mejor este proceso, suponga el caso del árbol de decisión mostrado en la Figura 3. 

<p align="center">
  <img width="300" alt="Visitados DFS" src="../resources/figures/treeCh01.png" />
   <br>
  <em>Figura 3: Árbol de búsqueda con nodo inicial A y nodo meta D. Las acciones están dadas por las letras en minúscula. Las acciones asociadas a backtracking se muestran como letras acompañadas de comilla simple (apóstrofo) y en color rojo.</em>
</p>

Los pasos a seguir por el algoritmo son los siguientes:

1. Se inserta el nodo inicial en la pila LIFO: [A].
2. Se extrae A de la pila y se marca como nodo visitado. Ya que el nodo A no es la meta, insertamos sus hijos en la pila y se marcan como visitados. La pila ahora es [B, C]. Es común que en las implementaciones en lenguajes de programación se denomine como pop y push a los procesos de extracción e inserción en la pila, respectivamente.
3. Si tenemos en cuenta que los nodos en la pila se van insertando de izquierda a derecha, entonces el nodo C es el último que entró. Por lo tanto, extraemos C. Ya que C no es el nodo meta, extraemos su único hijo que en este caso es F, lo ponemos en la pila y lo marcamos como visitado. La pila resultante es [B, F].
4. El siguiente nodo en ser extraído es el último en entrar (pila LIFO). Entonces extraemos F. Ya que no es el nodo meta, y no tiene hijos, se pasa a extraer el nodo B. Como se puede apreciar, en este paso hubo backtracking o retroceso, el cual no requirió manejo adicional debido a que está implícito en la forma en la que trabaja la pila LIFO.
5. Dado que el nodo B ya fue marcado como visitado, no se vuelve a insertar en la pila. El proceso de marcar a los nodos como visitados es muy importante cuando hay múltiples caminos al mismo nodo, esto evitará que el algoritmo se quede en un bucle infinito.
6. Se extrae el nodo B. Al no ser la meta, sus hijos, se marcan como visitados y se se extraen ponen en la pila, con lo cual se tiene [D, E].
7. E sale de la pila y se genera backtracking debido a que no tiene hijos y tampoco es la meta.
8. Solamente queda el nodo D. Dado que este es la meta, el algoritmo termina. La secuencia final de estados visitados es:

<p align="center">
  <img width="500" height="100" alt="Visitados DFS" src="../resources/figures/visitadosDFS.png" />
</p>

y las acciones que el agente debe ejecutar son {b,e,e’,b’,a,d,d’,c}. Los nodos que se muestran en gris y con línea punteada, son aquellos que ya se habían marcado como visitados y no ingresan a la pila LIFO por segunda vez, esto, tal como ya lo hemos dicho, con el fin de evitar bucles infinitos en el algoritmo.

La implementación computacional de DFS usada en nuestro simulador, está disponible en el siguiente enlace: <a href="https://github.com/daalmart/IA-ML-Book/blob/main/ch01/uninformed_search/dfs_bfs.ipynb">DFS.</a> En el enlace también encontrará ejemplos de uso para resolver problemas planteados como árboles de búsqueda.

### Breadth First Search
A diferencia del DFS, el algoritmo BFS hace una búsqueda del nodo meta hacia lo ancho del árbol. Para lograr esto, BFS se vale de una cola tipo FIFO, en la cual, el primer nodo en entrar es el primero en salir. En otras palabras, el comportamiento implícito en el proceso de inserción y extracción de este tipo de cola, garantiza que el árbol sea explorado hacia lo ancho y no hacia lo profundo como ocurre con DFS y su pila tipo LIFO. Para describir con mayor detalle el proceso, vamos a utilizar nuevamente el árbol mostrado en la Figura 3. Los pasos que el algoritmo sigue son los siguientes:
1. Se inserta el nodo inicial en la cola FIFO: [A].
2. Se extrae A de la cola y se marca como nodo visitado. Ya que el nodo A no es la meta, insertamos sus hijos en la cola y se marcan como visitados. La cola ahora es [B, C].
3. Si tenemos en cuenta que los nodos en la cola se van insertando de izquierda a derecha, entonces el nodo B fue el primero en entrar, por lo tanto, extraemos B. Ya que B no es el nodo meta, extraemos sus hijos, los ponemos en la cola y los marcamos como visitados. La pila resultante es [C, D, E].
4. El siguiente nodo en ser extraído es C, dado que ingresó antes que los nodos D y E. Ya que no es el nodo meta, extraemos su único hijo que es el nodo F, y lo ponemos en la cola, cuyo contenido ahora es [D, E, F].
5. Se extrae el nodo D. Dado que este es la meta, el algoritmo termina. La secuencia final de estados visitados es:

<p align="center">
  <img width="500" height="100" alt="Visitados BFS" src="../resources/figures/visitadosBFS.png" />
</p>

y las acciones que el agente debe ejecutar son {a,a’,b,b’,a,c}. Los nodos que se muestran en gris y con línea punteada, son aquellos que ya se habían marcado como visitados y no ingresan a la cola FIFO por segunda vez, esto, tal como ya lo hemos dicho, con el fin de evitar bucles infinitos en el algoritmo. Es importante tener en cuenta que en BFS no hay proceso de backtracking debido a que el algoritmo no se devuelve hacia los nodos padre. Si comparamos el número de nodos visitados en DFS y BFS, nos damos cuenta que BFS solamente visitó 3 nodos antes de llegar a la meta; por el contrario, DFS visitó 5, lo que supone que DFS toma más tiempo de ejecución para el caso de nuestro ejemplo. En términos de acciones ejecutadas, se puede apreciar que en BFS se tuvieron 6, 2 menos que en DFS.

### Uniform Cost Search
El algoritmo UCS, también conocido como búsqueda de costo uniforme, se basa en el mismo principio que el algoritmo de Dijkstra, propuesto por el matemático y científico
de la computación neerlandés Edsger W. Dijkstra, para encontrar caminos de costo mínimo desde un nodo de origen, considerando costos de transición no negativos. UCS utiliza una cola de prioridad en la cual los nodos con menor costo acumulado, es decir, los nodos cuya suma de costos de acciones en dirección al nodo inicial sea mínima, son los primeros en ser extraídos. De esta manera, a partir del nodo inicial, el algoritmo va almacenando en la cola de prioridad los nodos junto con sus respectivos costos acumulados, y selecciona para expansión aquel cuyo costo acumulado sea menor. Este proceso continúa hasta que el nodo meta es seleccionado para su expansión, es decir, hasta que es extraído de la cola. Para ilustrar este proceso, considere el ejemplo de la Figura 4, el cual representa una situación que podría enfrentar un vehículo autónomo cuyo objetivo es llegar desde la cuidad de Bogotá, al Valle de Sibundoy, en Colombia, utilizando dos rutas diferentes: una a través del departamento del Huila pasando por la ciudad
de Neiva y otra atravesando el departamento del Cauca, pasando por la ciudad de Popayán. Los pasos que el algoritmo ejecuta se muestran en la Tabla 1. Observe que la ruta que escogería el vehículo autónomo utilizando UCS es la que atraviesa el departamento del Cauca, dado que el costo acumulado de esta ruta es 29, mientras que la otra ruta acumula un costo de 30. Aunque este resultado puede parecer bastante obvio para un ser humano, es importante recordar que los algoritmos de inteligencia artificial, como los expuestos en este libro, constituyen herramientas que permiten dotar a los sistemas computacionales de mecanismos para analizar diferentes alternativas y seleccionar aquella que, de acuerdo con los criterios establecidos, resulte más conveniente.

<p align="center">
  <img width="400" alt="Visitados BFS" src="../resources/figures/UCS.png" />
   <br>
  <em>Figura 4: Árbol de búsqueda que representa el viaje de un vehículo autónomo desde Bogotá hasta el Valle de Sibundoy en Colombia. Los costos entre estados (nodos del árbol) se estiman a partir del estado histórico de las vías.</em>
</p>

| Paso | Nodo que se extrae | Nodo que ingresa – costo acumulado | Estado de la cola |
| :---: | :--- | :--- | :--- |
| 1 | – | Bogotá – 0 | `[(Bogotá, 0)]` |
| 2 | Bogotá | Melgar – 4, Girardot – 5 | `[(Melgar, 4), (Girardot, 5)]` |
| 3 | Melgar | Ibagué – 6 | `[(Girardot, 5), (Ibagué, 6)]` |
| 4 | Girardot | El Espinal – 7 | `[(Ibagué, 6), (El Espinal, 7)]` |
| 5 | Ibagué | Armenia – 13 | `[(El Espinal, 7), (Armenia, 13)]` |
| 6 | El Espinal | Neiva – 10 | `[(Neiva, 10), (Armenia, 13)]` |
| 7 | Neiva | Pitalito – 14 | `[(Armenia, 13), (Pitalito, 14)]` |
| 8 | Armenia | Cali – 15 | `[(Pitalito, 14), (Cali, 15)]` |
| 9 | Pitalito | Mocoa – 20 | `[(Cali, 15), (Mocoa, 20)]` |
| 10 | Cali | Popayán – 19 | `[(Popayán, 19), (Mocoa, 20)]` |
| 11 | Popayán | Pasto – 26 | `[(Mocoa, 20), (Pasto, 26)]` |
| 12 | Mocoa | Valle de Sibundoy – 30 | `[(Pasto, 26), (Valle de Sibundoy, 30)]` |
| 13 | Pasto | Valle de Sibundoy – 29 | `[(Valle de Sibundoy, 29), (Valle de Sibundoy, 30)]` |
| 14 | Valle de Sibundoy | – | `[(Valle de Sibundoy, 30)]` |

<p align="center"><em>Tabla 1: Evolución de la cola de prioridad durante la ejecución de UCS para el árbol de la Figura 4.</em></p>

La implementación computacional de UCS usada en nuestro simulador, está disponible en el siguiente enlace: <a href="https://github.com/daalmart/IA-ML-Book/blob/main/ch01/uninformed_search/ucs.ipynb">UCS.</a> En el enlace también encontrará ejemplos de uso para resolver problemas planteados como árboles de búsqueda.


