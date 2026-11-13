#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 11:26:59 2026

@author: kaluza
"""
import heapq
from collections import Counter

#DFS-Pila LIFO
def dfs(problema, inicio, meta):
    LIFO = [(inicio, [inicio])]
    visitados = set()

    while LIFO:#Retorna True si la pila tiene elementos.
        nodo, camino = LIFO.pop()#Retorna el último nodo que entró y el camino que llevó hasta él.

        if nodo == meta:
            return camino, visitados#Si el nodo es la meta, se retorna el camino que llevó a él y se termina el bucle.

        if nodo not in visitados:
            visitados.add(nodo)
            for sucesor in problema[nodo]:
                if sucesor not in visitados:
                    LIFO.append((sucesor, camino + [sucesor])#Se almacena cada sucesor y el camino que llevó a él (secuencia de nodos).
                                       )

    return None
#BFS-Pila FIFO
def bfs(problema, inicio, meta):
    FIFO = [(inicio, [inicio])]
    visitados = set()

    while FIFO:#Retorna True si la pila tiene elementos.
        nodo, camino = FIFO.pop(0)#Retorna el último nodo que entró y el camino que llevó hasta él.

        if nodo == meta:
            return camino, visitados#Si el nodo es la meta, se retorna el camino que llevó a él y se termina el bucle.

        if nodo not in visitados:
            visitados.add(nodo)

            for sucesor in problema[nodo]:
                if sucesor not in visitados:
                    FIFO.append(
                        (sucesor, camino + [sucesor])#Se almacena cada sucesor y el camino que llevó a él (secuencia de nodos).
                    )

    return None

def ucs(problema, inicio, meta):
    """
    algoritmo UCS con actualización de costos de nodos y control de nodos obsoletos.
    
    Args:
        problema: árbol o grafo de búsqueda.
        inicio: nodo inicial.
        meta: nodo meta.
    Returns:
        camino: ruta óptima a la meta.
        costo_actual: el costo acumulado óptimo.
        expansiones: diccionario con el número de veces que se expande cada nodo.
        costos: listado de costos acumulados de los nodos.
        None: cuando no hay solución.
    Raises:
        None.
    """
    
    priorityQueue = [(0, inicio, [inicio])]# Se crea la cola de prioridad con el costo del nodo inicial, el nodo inicial y su ruta
    costos = {inicio: 0}# Diccionario para actualizar costos acumulados
    expansiones = Counter()# Permite contar el número de veces que aparece un nodo

    while priorityQueue:
        costo_actual, nodo_actual, camino = heapq.heappop(priorityQueue)# Se extrae el costo, el nodo y la ruta hacia él

        if costo_actual > costos[nodo_actual]:
            continue

        if nodo_actual == meta:
            return camino, costo_actual, expansiones, costos

        expansiones[nodo_actual] += 1# Se incrementa cada vez que un nodo es expandido

    
        for sucesor, costo_accion in problema[nodo_actual]:#sucesor, costo_accion in problema.get(nodo_actual, []):#
            nuevo_costo = costo_actual + costo_accion

            if (sucesor not in costos or
                    nuevo_costo < costos[sucesor]): # Se actualizan costos de nodos cuando hay rutas mejores hacia ellos
                costos[sucesor] = nuevo_costo

                heapq.heappush(
                    priorityQueue,
                    (nuevo_costo, sucesor, camino + [sucesor])
                )

    return None

