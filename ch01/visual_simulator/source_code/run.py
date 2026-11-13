import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup, Node
from pellets import PelletGroup
import time
from uninformed_search import dfs,bfs,ucs
import sys
import pygame_menu
from pygame_menu.locals import ALIGN_LEFT
import math
from informed_search import gbfs
import tkinter as tk
import threading
from tkinter import simpledialog
import time

# import faulthandler
# faulthandler.enable()

class GameController(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Algoritmos de Búsqueda.")
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.tree={}
        self.tree_with_costs={}
        self.directions={}
        self.maze='simple'
        
        self.time_dfs=0
        self.time_bfs=0
        self.time_ucs=0
        self.time_gbfs_eu=0
        self.time_gbfs_mh=0
        
        self.visitados_dfs=0
        self.visitados_bfs=0
        self.visitados_ucs=0
        self.visitados_gbfs_eu=0
        self.visitados_gbfs_mh=0
        
        self.costo_ucs=0
        self.costo_astar=0
        
        self.crear_menu_encabezado()
        self.ucs=False
        self.gbfs_mh=False
        self.gbfs_eu=False

    def reset_metrics(self):
        self.time_dfs=0
        self.time_bfs=0
        self.time_ucs=0
        self.time_gbfs_eu=0
        self.time_gbfs_mh=0
        
        self.visitados_dfs=0
        self.visitados_bfs=0
        self.visitados_ucs=0
        self.visitados_gbfs_eu=0
        self.visitados_gbfs_mh=0
        
        self.costo_ucs=0
        self.costo_astar=0
    
    def lanzar_ventana_estadisticas(self, nodos_visitados, tiempo_ms, costo):
    
        # 1. Definir la construcción de la ventana como una función interna
        def crear_ventana():
            ventana = tk.Tk()
            ventana.title("Resultados de Búsqueda")
            ventana.geometry("300x200")
            
            tk.Label(ventana, text=f"Nodos expandidos: {nodos_visitados}").pack(pady=5)
            tk.Label(ventana, text=f"Tiempo de ejecución: {tiempo_ms} ms").pack(pady=5)
            tk.Label(ventana, text=f"Costo del camino: {costo}").pack(pady=5)
            
            tk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=15)
            
            # Este mainloop ahora atrapa únicamente a este hilo, liberando a Pygame
            ventana.mainloop() 
    
        # 2. Configurar y arrancar el hilo independiente
        # daemon=True asegura que si cierras Pygame abruptamente, esta ventana también se destruya
        hilo_tkinter = threading.Thread(target=crear_ventana, daemon=True)
        hilo_tkinter.start()
    
   
    def crear_menu_encabezado(self):
        
        
        if self.maze=='complex':
            screen_size=SCREENSIZE_CM
            width_fp=928
            height_fp=520
        else:
            screen_size=SCREENSIZE
            width_fp=448
            height_fp=520
        theme_m = pygame_menu.themes.THEME_DARK.copy()

        theme_m.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        theme_m.background_color = (0, 0, 0, 0) # Negro con transparencia
        theme_m.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        theme_m.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        theme_m.widget_margin = (0, 0)  # <--- Elimina espacios invisibles del tema
        theme_m.title_font_size = 1 # Reducir el título aunque esté oculto


        # Crear el menú principal
        self.menu = pygame_menu.Menu(
            title='', 
            width=screen_size[0],
            height=screen_size[1],
            center_content=False,       # Envía todo hacia la parte superior
            rows=1,              
            columns=1,
            theme=theme_m
        )

        # 1. Instanciar el Frame directamente
       
        frame_principal = pygame_menu.widgets.Frame(
            width=width_fp,
            height=height_fp,
            orientation=pygame_menu.locals.ORIENTATION_VERTICAL
        )

      
        frame_principal.set_margin(0, 0)
        self.menu.add.generic_widget(frame_principal)

        estilo_compacto = {
            'font_size': 12,
            'margin': (0, 1), 
            'padding': 1
        }

        opciones_dificultad = [('DFS', 1), ('BFS', 2), ('UCS', 3),('GBFS-MH', 4),('GBFS-EU', 5)]
        
        theme_results=pygame_menu.themes.THEME_GREEN
        theme_results.title_font_size = 32
        self.menuResults = pygame_menu.Menu(title="Resultados",
                           width=SCREENSIZE[0],
                           height=SCREENSIZE[1],
                           position=(0, 0, False),
                           theme=theme_results
                           )
        
        self.menuResults.get_menubar().set_onreturn(self.accion_flecha_back)
        
        # 1. Agregar la imagen al menú
        
        imagen_esquina = self.menuResults.add.image(
            'robot-removebg.png',
            scale=(0.2, 0.2), # Ajusta el decimal (ej. 0.5) si la imagen es muy grande
            align=ALIGN_LEFT
        )
        
        # 2. Hacer que flote desde el origen (esquina superior izquierda absoluta)
        # Al ser flotante, no empujará los demás widgets (tablas, títulos) hacia abajo
        imagen_esquina.set_float(True, origin_position=True)
        
        # 3. (Opcional) Separarla levemente del borde para que no quede pegada (X, Y)
        imagen_esquina.translate(15, 15)
        
        # self.menuResults.add.button(title="Main",
        #                     font_color=WHITE, background_color=GREEN)

        drop_select_alg = self.menu.add.dropselect(
            title='Algoritmo:',
            items=opciones_dificultad,
            #default=1,
            placeholder='Seleccionar',
            **estilo_compacto,
            onchange=self.ejecutar_algoritmo
        )
        
        opciones_laberinto = [('Simple', 1), ('Complejo', 2)]
        drop_select_lab = self.menu.add.dropselect(
            title='Laberinto:',
            items=opciones_laberinto,
            #default=0,
            placeholder='Seleccionar',
            **estilo_compacto,
            onchange=self.cambiar_laberinto
        )

        boton_resultados = self.menu.add.button(
            title='Resultados',
            action=self.accion_resultados,#self.menuResults,
            **estilo_compacto
        )

        frame_principal.pack(drop_select_alg, align=pygame_menu.locals.ALIGN_LEFT)
        frame_principal.pack(drop_select_lab, align=pygame_menu.locals.ALIGN_LEFT)
        frame_principal.pack(boton_resultados, align=pygame_menu.locals.ALIGN_LEFT)
        

        
        tabla_resultados = self.menuResults.add.table(table_id='tabla_stats', font_size=14)

        # 2. Configurar el diseño predeterminado de las celdas
        tabla_resultados.default_cell_padding = 10
        tabla_resultados.default_row_background_color = (50, 50, 50, 150) # Fondo oscuro semitransparente
        tabla_resultados.default_cell_border_color = (255, 255, 255) # Bordes blancos
        tabla_resultados.default_cell_border_width = 1
        
        # 3. Añadir la fila de encabezados
        tabla_resultados.add_row(
            ['Algoritmo', 'Nodos Visitados', 'Costo', 'Tiempo [\u03bcs]'], 
            cell_font_color=(255, 255, 0) # Texto amarillo para destacar los títulos
        )
        
        # 4. Añadir las filas de datos extraídas de tus ejecuciones
        time_scale=1000000
        tabla_resultados.add_row(['DFS', f'{self.visitados_dfs}', '-', f'{(self.time_dfs*time_scale):0.2f}'])
        tabla_resultados.add_row(['BFS', f'{self.visitados_bfs}', '-', f'{(self.time_bfs*time_scale):0.2f}'])
        tabla_resultados.add_row(['UCS', f'{self.visitados_ucs}', '450', f'{(self.time_ucs*time_scale):0.2f}'])
        tabla_resultados.add_row(['GBFS-EU', f'{self.visitados_gbfs_eu}', '-', f'{(self.time_gbfs_eu*time_scale):0.2f}'])
        tabla_resultados.add_row(['GBFS-MH', f'{self.visitados_gbfs_mh}', '-', f'{(self.time_gbfs_mh*time_scale):0.2f}'])
        tabla_resultados.add_row(['A*', '45', '120', '3.5'])

        
        #self.menuResults.add.button("Main", self.lanzar_ventana_estadisticas, 12, 12, 12, font_color=WHITE, background_color=GREEN)
        # self.menuConfig = pygame_menu.Menu(title="Configuración",
        #                    width=SCREENSIZE[0],#screen_size[0],
        #                    height=SCREENSIZE[1],#screen_size[1],
        #                    theme=theme_results
        #                    )
        #self.menuConfig.add.button("Configuraciones", font_color=WHITE, background_color=GREEN)
        
        
        #self.menuResults.add.button("Configuración", action=self.menuConfig, font_color=WHITE, background_color=GREEN)
    '''Permite regresar del menú de resultados al complex maze o al simple maze.'''    
    def accion_flecha_back(self):      
        if self.maze=='complex':
            self.screen = pygame.display.set_mode(SCREENSIZE_CM, 0, 32)
        self.menu.reset(1)
    
    '''Se llama desde el botón de ver resultados para que siempre se vea el menú de resultados del mismo tamaño.'''
    def accion_resultados(self):
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.menu._open(self.menuResults)


    '''cambia el maze de simple a complex.'''
    def cambiar_laberinto(self, valor_seleccionado, id_opcion):
        print('Cambiando laberinto')
        if id_opcion==1:
            print('Sencillo')
            self.maze='simple'
            self.reset_metrics()

        elif id_opcion==2:
            print('Complex')
            self.maze='complex'
            self.reset_metrics()
        
        self.setBackground()
       
    '''Permite seleccionar el algoritmo a ejecutar'''
    def ejecutar_algoritmo(self, valor_seleccionado, id_opcion):
        self.pacman = Pacman(self.ni)
        self.ucs=False
        self.gbfs_mh=False
        self.gbfs_eu=False
        if id_opcion == 1:
            self.run_dfs()
        elif id_opcion == 2:
            self.run_bfs()
        elif id_opcion == 3:
            self.ucs=True
            self.run_ucs()
        elif id_opcion == 4:
            self.gbfs_mh=True
            self.run_gbfs_mh()
        elif id_opcion == 5:
            self.gbfs_eu=True
            self.run_gbfs_eu()
        
        self.crear_menu_encabezado()
       

    def setBackground(self):
        
        
        if self.maze=='simple':
            imagen_fondo = pygame.image.load('modelBased_sin_ag_sin_lin.png').convert()
            self.background = pygame.transform.scale(imagen_fondo, SCREENSIZE)
            self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
            self.nodes = NodeGroup("maze_costos.txt")            
            self.ni=self.nodes.getNodeFromTiles(2,27)
            self.nf=self.nodes.getNodeFromTiles(25,5)
        else:
            imagen_fondo = pygame.image.load('complex_maze.jpeg').convert()
            self.background = pygame.transform.scale(imagen_fondo, SCREENSIZE_CM)
            self.screen = pygame.display.set_mode(SCREENSIZE_CM, 0, 32)
            self.nodes = NodeGroup("maze_complex_costos.txt")
            #print('nodos del complex',self.nodes)
            self.ni=self.nodes.getNodeFromTiles(5,52)
            self.nf=self.nodes.getNodeFromTiles(54,5)
        #imagen_fondo = pygame.image.load('complex_maze.jpeg').convert()
        # Asigna la imagen ya escalada directamente a self.background
        
        #
        self.crear_menu_encabezado()
        
        # if self.maze=='simple':
        #     self.nodes = NodeGroup("maze_costos.txt")            
        #     self.ni=self.nodes.getNodeFromTiles(2,27)
        #     self.nf=self.nodes.getNodeFromTiles(25,5)

        # else:
        #     self.nodes = NodeGroup("maze_complex_costos.txt")
        #     print('nodos del complex',self.nodes)
        #     self.ni=self.nodes.getNodeFromTiles(5,52)
        #     self.nf=self.nodes.getNodeFromTiles(54,5)

        self.ucs_cost_coordinates=[]
        self.camino=[]
        self.visitados=[]
        self.heuristic_coordinates_eu=[]
        self.heuristic_coordinates_mh=[]  
        self.pacman = Pacman(self.ni)        

    
    
      
    def startGame(self): 
        self.setBackground()
        # if ucs:
        #     self.nodes = NodeGroup("maze_costos.txt")
        
        self.nodes = NodeGroup("maze_costos.txt")
        
        self.ni=self.nodes.getNodeFromTiles(2,27)
        self.nf=self.nodes.getNodeFromTiles(25,5)
           
            
            
        self.pacman = Pacman(self.ni)        
     
        #self.run_bfs()
    
    
    def run_gbfs_mh(self):
        heuristics = {}
        for k_node, node in self.nodes.getNodes().items(): #k:tupla con posición, v es el nodo.
            heu=self.heuristica_manhattan(node,self.nf)
            heuristics[node]=heu
            self.heuristic_coordinates_mh.append((node.position.x,node.position.y,str(f'{heu:.2f}'))) 
            
            neighbors = node.getNeighbors() 
            neigs = []
            for _, neig in neighbors.items(): 
                if neig is not None:
                    neigs.append(neig) 
                     
              
            self.tree[node] = neigs
            
        inicio = time.perf_counter()
        self.camino,self.visitados=gbfs(self.tree,self.ni,self.nf, heuristics)#(nf.getPosition().x,nf.getPosition().y))
        fin = time.perf_counter()
        self.visitados_gbfs_mh=len(self.visitados)
        self.time_gbfs_mh=fin - inicio
        print(f"Tiempo de ejecución GBFS-MH: {(fin - inicio):.8f} segundos")
        self.pacman.setPath(self.camino)
        
    def run_gbfs_eu(self):
        heuristics = {}
        for k_node, node in self.nodes.getNodes().items(): #k:tupla con posición, v es el nodo.
            heu=self.heuristica_euclidiana(node,self.nf)
            heuristics[node]=heu
            self.heuristic_coordinates_eu.append((node.position.x,node.position.y,str(f'{heu:.2f}'))) 
            
            neighbors = node.getNeighbors() 
            neigs = []
            for _, neig in neighbors.items(): 
                if neig is not None:
                    neigs.append(neig) 
                     
              
            self.tree[node] = neigs
        inicio = time.perf_counter()
        self.camino,self.visitados=gbfs(self.tree,self.ni,self.nf, heuristics)#(nf.getPosition().x,nf.getPosition().y))
        fin = time.perf_counter()
        self.time_gbfs_eu=fin - inicio
        self.visitados_gbfs_eu=len(self.visitados)
        print(f"Tiempo de ejecución GBFS-EU: {(fin - inicio):.8f} segundos")
        self.pacman.setPath(self.camino)
        
    def run_bfs(self):
        for k, v in self.nodes.getNodes().items(): #k:tupla con posición, v es el nodo.
             neighbors = v.getNeighbors() 
             neigs = []
             for _, neig in neighbors.items(): 
                 if neig is not None:
                     neigs.append(neig) 
              
             self.tree[v] = neigs
        inicio = time.perf_counter()
        self.camino,self.visitados=bfs(self.tree,self.ni,self.nf)#(nf.getPosition().x,nf.getPosition().y))
        fin = time.perf_counter()
        self.time_bfs=fin - inicio
        self.visitados_bfs=len(self.visitados)
        print(f"Tiempo de ejecución BFS: {(fin - inicio):.8f} segundos")

        self.pacman.setPath(self.camino)

    def run_dfs(self):
         for k, v in self.nodes.getNodes().items(): #k:tupla con posición, v es el nodo.
              neighbors = v.getNeighbors() 
              neigs = []
              for _, neig in neighbors.items(): 
                  if neig is not None:
                      neigs.append(neig) 
               
              self.tree[v] = neigs
         inicio = time.perf_counter()
         self.camino,self.visitados=dfs(self.tree,self.ni,self.nf)#(nf.getPosition().x,nf.getPosition().y))
         fin = time.perf_counter()
         self.time_dfs=fin - inicio
         self.visitados_dfs=len(self.visitados)
         print(f"Tiempo de ejecución DFS: {(fin - inicio):.8f} segundos")
         self.pacman.setPath(self.camino)   

    def run_ucs(self):
        for fath_key, fath in self.nodes.getNodes().items(): #k:tupla con posición, v es el nodo.
            neighbors = fath.getNeighbors() 
            neigs_cost = list()
            for _, neig in neighbors.items(): 
                if neig is not None:
                    x_res,y_res=(neig.getPosition()-fath.getPosition()).asTuple()
                    
                    if x_res==0:#Están en la misma columna
                        #print(f'El y del neig es {neig.getPosition().y}, el y del fath es {fath.getPosition().y}')
                        costo=-10
                        for y in range(min(neig.getPosition().y, fath.getPosition().y),max(neig.getPosition().y, fath.getPosition().y)+1): 
                            try:
                                #print('Este es el Y',y)
                                costo=int(self.nodes.getMazeCosts()[(neig.getPosition().x,y)])
                                #print(f'Costo encontrado: {costo}, entre los nodos {fath} y {neig}')
                                neigs_cost.append((neig,costo))
                                self.ucs_cost_coordinates.append((neig.getPosition().x,y,str(costo)))                                
                            except KeyError:#Se lanza cada vez que un y entre neig y fath no tiene número.
                                pass#print('No hay costos entre esos nodos.')
                                #neigs_cost.append((neig,1))#pass#No hay costos entre esos nodos.
                        # if costo==-10:
                        #     neigs_cost.append((neig,1))
                    elif y_res==0:#Están en la misma fila
                       costo=-10
                       for x in range(min(neig.getPosition().x, fath.getPosition().x),max(neig.getPosition().x, fath.getPosition().x)+1): 
                           try:
                               costo=int(self.nodes.getMazeCosts()[(x,neig.getPosition().y)])
                               #print(f'Costo encontrado: {costo}, entre los nodos {fath} y {neig}')
                               neigs_cost.append((neig,costo))
                               self.ucs_cost_coordinates.append((x, neig.getPosition().y,str(costo)))
                           except KeyError:
                               pass#print('No hay costos entre esos nodos.')
                               #neigs_cost.append((neig,1))#pass#No hay costos entre esos nodos.
                       # if costo==-10:
                       #     neigs_cost.append((neig,1))
            #print('lista cost-neigs',neigs_cost)
            if neigs_cost:
                self.tree_with_costs[fath] = neigs_cost  
               
        # for k,v in self.tree_with_costs.items():
        #     print('padre',k)
        #     for neig in v:
        #         print('hijo:',neig[0])
        #         print('costo:',neig[1])
        
        self.nodes.setPortalPair((0, 17), (27, 17)) 
        self.pellets = PelletGroup("maze_costos.txt") 
            
        inicio = time.perf_counter()
        self.camino,_,expansiones,_=ucs(self.tree_with_costs,self.ni,self.nf)#(nf.getPosition().x,nf.getPosition().y))
        fin = time.perf_counter()
        self.time_ucs=fin - inicio
        self.visitados_ucs=len(self.visitados)
        print(f"Tiempo de ejecución UCS: {(fin - inicio):.8f} segundos")
        self.visitados=list(expansiones)
        self.pacman.setPath(self.camino)
    def dibujar_ruta_transparente(self, lista_nodos):
        # 1. Crear una superficie del tamaño de la pantalla con soporte para canal Alfa (SRCALPHA)
        ancho, alto = self.screen.get_size()
        superficie_trazos = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        
        # 2. Extraer las coordenadas x, y de la lista de objetos Nodo
        coordenadas = [(nodo.position.x, nodo.position.y) for nodo in lista_nodos]
        
        # 3. Definir el color usando RGBA (Rojo, Verde, Azul, Alfa)
        # El valor Alfa va de 0 (invisible) a 255 (totalmente opaco). 
        # (0, 255, 255, 120) generará una línea color cyan semitransparente.
        color_ruta = (0, 255, 255, 120)
        grosor = 6
        
        # 4. Dibujar una secuencia de líneas continuas sobre la superficie temporal
        # El tercer parámetro (False) indica que no queremos cerrar la figura uniendo el último nodo con el primero
        if len(coordenadas) > 1:
            pygame.draw.lines(superficie_trazos, color_ruta, False, coordenadas, grosor)
            
        # 5. Dibujar la superficie temporal con las líneas sobre la pantalla principal
        self.screen.blit(superficie_trazos, (0, 0))
    
    def dibujar_visitados(self, lista_nodos):
        
        radio = 8
        
        # 2. Crear una superficie temporal del tamaño exacto del círculo (diámetro x diámetro) con soporte Alfa[cite: 21]
        superficie_temp = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
        color_ruta = (0, 0, 255, 120)

        for n in lista_nodos:
            if n is not None:
                pygame.draw.circle(superficie_temp, color_ruta, (radio, radio), radio)

                x, y = n.position.asInt()

                # 5. Ajustar la posición para que el blit quede perfectamente centrado
                pos_x = x - radio
                pos_y = y - radio
                
                # 6. Dibujar la superficie temporal con el círculo sobre la pantalla principal[cite: 21]
                self.screen.blit(superficie_temp, (pos_x, pos_y))
                #pygame.draw.circle(self.screen, color_ruta, n.position.asInt(), 8)
    
    def heuristica_manhattan(self, nodo_actual, nodo_meta):
        # Asumiendo que nodo_actual y nodo_meta son instancias de tu clase Node
        x_actual, y_actual = nodo_actual.position.x, nodo_actual.position.y
        x_meta, y_meta = nodo_meta.position.x, nodo_meta.position.y
    
        return abs(x_actual - x_meta) + abs(y_actual - y_meta)
    def heuristica_euclidiana(self, nodo_actual, nodo_meta):
        x_actual, y_actual = nodo_actual.position.x, nodo_actual.position.y
        x_meta, y_meta = nodo_meta.position.x, nodo_meta.position.y
        
        return math.sqrt((x_actual - x_meta)**2 + (y_actual - y_meta)**2)

    def update(self):
        dt = self.clock.tick(30) / 1000.0

        self.pacman.update(dt)
        #self.pellets.update(dt)
        #self.checkPelletEvents()
        self.checkEvents()
        self.render()  
        
    def cambiar_nodo_inicial(self, posicion_mouse):
        columna = posicion_mouse[0] // TILEWIDTH
        fila = posicion_mouse[1] // TILEHEIGHT
        
        # Buscar el nodo en esa posición de la cuadrícula
        nuevo_nodo_inicial = self.nodes.getNodeFromTiles(columna, fila)
        
        if nuevo_nodo_inicial is not None:
            # Reasignar el objeto Pacman (el carrito) a este nuevo nodo
            self.ni=nuevo_nodo_inicial
            self.pacman = Pacman(nuevo_nodo_inicial)
            
    def verificar_clic_costo(self, posicion_mouse):
        # Iterar sobre todos los nodos extraídos del diccionario[cite: 1]
       columna = posicion_mouse[0] // TILEWIDTH
       fila = posicion_mouse[1] // TILEHEIGHT
       
       # Buscar el nodo en esa posición de la cuadrícula
       cost_node = self.nodes.getCostNodeFromTiles(columna, fila)
       
       if cost_node is not None:
           self.pedir_nuevo_costo(cost_node)
                
                
    def pedir_nuevo_costo(self, nodo):
        def abrir_input():
            root = tk.Tk()
            root.withdraw() # Ocultar la ventana de fondo blanca, mostrar solo el diálogo
            
            # Lanzar una alerta nativa para escribir el nuevo número
            nuevo_valor = simpledialog.askinteger("Costo", f"Nuevo costo para la transición:", initialvalue=self.nodes.getMazeCosts()[(nodo.getPosition().x,nodo.getPosition().y)])
            
            if nuevo_valor is not None:
                self.ucs_cost_coordinates.append((nodo.getPosition().x, nodo.getPosition().y,str(nuevo_valor)))
                self.nodes.getMazeCosts()[(nodo.getPosition().x, nodo.getPosition().y)]=str(nuevo_valor)
            root.destroy()
            
        # Ejecutar en un hilo paralelo (daemon=True) para no bloquear el bucle de renderizado de Pygame[cite: 1]
        hilo = threading.Thread(target=abrir_input, daemon=True)
        hilo.start()

    def checkEvents(self):
        events=pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Detectar clic del ratón
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clic izquierdo
                    # Obtener la tupla de coordenadas (x, y) del clic
                    mouse_pos = pygame.mouse.get_pos()
                    self.cambiar_nodo_inicial(mouse_pos)
                elif event.button == 3:
                    mouse_pos = event.pos # Tupla con las coordenadas (x, y) del clic
                    print('Click derecho',mouse_pos)
                    self.verificar_clic_costo(mouse_pos)
        # Actualizar el menú superpuesto
        if self.menu.is_enabled():
            self.menu.update(events)
        # if self.menuResults.is_enabled():
        #     self.menuResults.update(events)

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)
            
    def actualizar_costos(self):
        for cd in self.ucs_cost_coordinates:
            pygame.draw.circle(self.screen, RED, (cd[0],cd[1]), 10)
            fuente = pygame.font.SysFont(None, 16) 
            superficie_texto = fuente.render(cd[2], True, (255, 255, 255)) # Texto en color blanco
            rect_texto = superficie_texto.get_rect(center=(cd[0],cd[1]))
            self.screen.blit(superficie_texto, rect_texto)
   
    def dibujar_estrella(self, superficie, color, centro, radio_exterior, radio_interior):
        puntos_estrella = []
        cx, cy = centro
        
        # Una estrella de 5 puntas requiere 10 vértices (5 externos, 5 internos)
        for i in range(10):
            # Alternar entre el radio de las puntas y el radio de los valles
            radio_actual = radio_exterior if i % 2 == 0 else radio_interior
            
            # Calcular el ángulo para cada vértice (math.pi / 5 es 36 grados)
            # Se resta math.pi / 2 (90 grados) para que la primera punta quede exactamente hacia arriba
            angulo = i * (math.pi / 5) - (math.pi / 2)
            
            # Calcular las coordenadas X e Y usando seno y coseno
            x = cx + radio_actual * math.cos(angulo)
            y = cy + radio_actual * math.sin(angulo)
            
            puntos_estrella.append((x, y))
            
        # Dibujar el polígono con los vértices calculados
        pygame.draw.polygon(superficie, color, puntos_estrella, 2)

    def render(self):
        menu_actual = self.menu.get_current()
        if menu_actual==self.menu:
            self.screen.blit(self.background, (0, 0))
            self.nodes.render(self.screen)
            #self.pellets.render(self.screen)
            
            # 3. Dibujar el menú en el encabezado (encima de todo)
            if self.menu.is_enabled():
                self.menu.draw(self.screen)            
            if self.ucs:
                #self.actualizar_costos()
                for cd in self.ucs_cost_coordinates:
                    # puntos_poligono = [
                    #     (cd[0], cd[1] - 10), 
                    #     (cd[0] + 10, cd[1]), 
                    #     (cd[0], cd[1] + 10), 
                    #     (cd[0] - 10, cd[1])
                    # ]
                    # pygame.draw.polygon(self.screen, RED, puntos_poligono,2)
                    self.dibujar_estrella(self.screen, YELLOW, (cd[0], cd[1]), 12, 6)
                    #pygame.draw.circle(self.screen, RED, (cd[0],cd[1]), 10)
                    fuente = pygame.font.SysFont(None, 16) 
                    superficie_texto = fuente.render(cd[2], True, (255, 255, 255)) # Texto en color
                    rect_texto = superficie_texto.get_rect(center=(cd[0],cd[1]))
                    self.screen.blit(superficie_texto, rect_texto)
            elif self.gbfs_mh:
                for hc in self.heuristic_coordinates_mh:
                    #pygame.draw.circle(self.screen, RED, (cd[0],cd[1]), 10)
                    fuente = pygame.font.SysFont(None, 16) 
                    superficie_texto = fuente.render(hc[2], True, (255, 255, 255)) # Texto en color blanco
                    self.rect_texto_costo = superficie_texto.get_rect(center=(hc[0],hc[1]))
                    self.screen.blit(superficie_texto, self.rect_texto_costo)                 
            elif self.gbfs_eu:
                for hc in self.heuristic_coordinates_eu:
                    #pygame.draw.circle(self.screen, RED, (cd[0],cd[1]), 10)
                    fuente = pygame.font.SysFont(None, 16) 
                    superficie_texto = fuente.render(hc[2], True, (255, 255, 255)) # Texto en color blanco
                    rect_texto = superficie_texto.get_rect(center=(hc[0],hc[1]))
                    self.screen.blit(superficie_texto, rect_texto)
            
            self.dibujar_ruta_transparente(self.camino)
            self.dibujar_visitados(self.visitados)
            self.pacman.render(self.screen)
            
        elif menu_actual==self.menuResults:               
            if self.menuResults.is_enabled():
                 self.menuResults.draw(self.screen)
        else:
            if self.menuConfig.is_enabled():
                 self.menuConfig.draw(self.screen)

        pygame.display.update()

    
if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()