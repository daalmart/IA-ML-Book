#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 10:19:53 2026

@author: kaluza
"""

import heapq


def gbfs(problema, inicio, meta, h):
	# Cola de prioridad con la heurística del nodo inicial, el nodo inicial y el camino hacia el nodo inicial.
    priorityQueue = [(h[inicio], inicio, [inicio])]
    visitados = set()

    while priorityQueue:
    	# Con heappop se extrae el mínimo valor de heurística, el nodo correspondiente y el camino para llegar a él.
        heuristica, nodo, camino = heapq.heappop(priorityQueue)
        if nodo == meta:
            return camino, visitados
		# Si se cumple esta condición, inicia un nuevo ciclo while.
        if nodo in visitados:
            continue

        visitados.add(nodo)

        for sucesor in problema[nodo]:
            if sucesor not in visitados:
                nuevo_camino = camino + [sucesor]
				# Se inserta el sucesor, su heurística y el camino que lleva a él en la cola de prioridad.
                heapq.heappush(
                    priorityQueue,
                    (h[sucesor], sucesor, nuevo_camino)
                )

    return None