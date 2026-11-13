import pygame
from pygame.locals import *
from vector import Vector2
from constants import *

class Pacman(object):
    def __init__(self, node):
        self.name = PACMAN
        self.directions = {STOP:Vector2(), UP:Vector2(0,-1), DOWN:Vector2(0,1), LEFT:Vector2(-1,0), RIGHT:Vector2(1,0)}
        self.direction = STOP
        self.speed = 100 * TILEWIDTH/16
        self.radius = 35
        self.color = YELLOW
        self.node = node
        self.setPosition()
        self.target = node
        self.collideRadius = 5
        
        self.imagen_carro = pygame.image.load('agente_removebg.png').convert_alpha()
        
        # 2. Definir el color blanco puro como transparente usando su valor RGB
        #color_rojo = (255, 0, 0)
        #self.imagen_carro.set_colorkey(color_rojo)
        
        # 2. Escalar la imagen (Opcional pero recomendado)
        # El diámetro del círculo original es self.radius * 2
        diametro = self.radius * 2
        self.imagen_carro = pygame.transform.scale(self.imagen_carro, (diametro, diametro))

    def setPosition(self):
        self.position = self.node.position.copy()

    # def update(self, dt):	
    #     self.position += self.directions[self.direction]*self.speed*dt
    #     direction = self.getValidKey()
    #     if self.overshotTarget():
    #         self.node = self.target
    #         if self.node.neighbors[PORTAL] is not None:
    #             self.node = self.node.neighbors[PORTAL]
    #         self.target = self.getNewTarget(direction)
    #         if self.target is not self.node:
    #             self.direction = direction
    #         else:
    #             self.target = self.getNewTarget(self.direction)
    #         if self.target is self.node:
    #             self.direction = STOP
    #         self.setPosition()
    #     else: 
    #         if self.oppositeDirection(direction):
    #             self.reverseDirection()
        
    
    # Agrega esto en la inicialización o como métodos nuevos en Pacman
    def setPath(self, path):
        self.path = path # Lista de nodos a visitar
        if self.path:
            self.target = self.path.pop(0)
            self.direction = self.getDirectionToTarget(self.node, self.target)#self.dirn.pop(0)#

    def getDirectionToTarget(self, current_node, target_node):
        # Compara las posiciones para saber qué dirección tomar (UP, DOWN, LEFT, RIGHT)
        cx, cy = current_node.position.x,current_node.position.y
        tx, ty = target_node.position.x, target_node.position.y
        
        if tx > cx: return RIGHT 
        if tx < cx: return LEFT
        if ty > cy: return DOWN
        if ty < cy: return UP
        return STOP

    def update(self, dt):     
        self.position += self.directions[self.direction] * self.speed * dt 
        
        if self.overshotTarget(): 
            self.node = self.target 
            if self.node.neighbors[PORTAL] is not None: 
                self.node = self.node.neighbors[PORTAL] 
            
            # Obtener el siguiente nodo de la lista automáticamente
            if hasattr(self, 'path') and len(self.path) > 0:
                self.target = self.path.pop(0)
                self.direction = self.getDirectionToTarget(self.node, self.target)
            else:
                self.target = self.node
                self.direction = STOP # Detenerse si no hay más nodos
                
            self.setPosition()
            
    def validDirection(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP
    
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False
    
    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def oppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False
    
    def eatPellets(self, pelletList):
        for pellet in pelletList:
            d = self.position - pellet.position
            dSquared = d.magnitudeSquared()
            rSquared = (pellet.radius+self.collideRadius)**2
            if dSquared <= rSquared:
                return pellet
        return None

    # def render(self, screen):
    #     p = self.position.asInt()
    #     pygame.draw.circle(screen, self.color, p, self.radius)
        
    def render(self, screen):
        # Obtener la posición central (como lo tenías)
        p = self.position.asInt()
        #print('Pacman position: ',p)
        
        # Calcular la esquina superior izquierda para centrar la imagen
        esquina_x = p[0] - self.radius
        esquina_y = p[1] - self.radius
        #self.imagen_carro = pygame.image.load('agente.jpeg').convert()
        # 2. Definir el color blanco puro como transparente usando su valor RGB
        #color_blanco = (255, 255, 255)
        #self.imagen_carro.set_colorkey(color_blanco)
        # Dibujar la imagen en la pantalla
        screen.blit(self.imagen_carro, (esquina_x, esquina_y))