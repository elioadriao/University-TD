# -*- coding: latin1 -*-
#-Helio A. Adriao dos Santos-#
#----------------------------#

import pygame
import rectangle
import time

class MobLife:
    def __init__(self, pos, max_health):
        self.max_health = max_health
        self.position = pos
        self.current_health = max_health
        self.width = 20
        self.height = 5
        self.current_width = 20
        self.bg_color = (225, 0, 0)
        self.color = (0, 225, 0)
        self.place_bar()

    #-Posiciona o retangulo do hp
    def place_bar(self):
        self.bg = pygame.rect.Rect(self.position, (self.width, self.height))
        self.current = pygame.rect.Rect(self.position, (self.current_width, self.height))

    #-Atualiza o valor do HP
    def update_health(self, value):
        if self.current_health != value:
            self.current_health = value
            perc = float(self.current_health) / self.max_health
            self.current_width = min(self.width, self.width*perc)

    def set_position(self, pos):
        self.position = pos
        self.place_bar()

    def draw_this(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.bg)
        pygame.draw.rect(surface, self.color, self.current)

class Mob(rectangle.Rectangle):
    #-Codigo usado no reconhecimento do mob ao ler no arquivo de level
    ident = "trabalho"
    #-Inicializa o Mob padrao
    def __init__(self, position, health=100, name="Trabalho", speed=75, image="files/mob.png", value=15):
        rectangle.Rectangle.__init__(self, 34, position, 16, 16, image)
        self.health = self.max_health = health
        self.speed = speed
        self.value = value
        self.destinations = []
        self.visited = 0
        self.name = name
        self.last_frame = time.time()
        self.dt = 0
        self.setup_life()

    #-Inicializa a barra de HP
    def setup_life(self):
        health_pos = self.position[0] + .5* self.width - .5*20, self.position[1] - 5 - 3
        self.healthbar = MobLife(health_pos, self.max_health)

    def draw_life(self, surface):
        self.healthbar.draw_this(surface)

    #-Coloca a barra sempre encima do mob
    def follow_mob_pos(self):
        self.healthbar.set_position((self.position[0] + .5* self.width - .5*20, self.position[1] - 5 - 3))

    #-Retorna as informacoes para o display
    def get_info(self):
        info = []
        line = "Nome: %s" %(self.name)
        info.append(line)
        line = "Vida: %s" %(self.health)
        info.append(line)
        line = "Valor: $%s" %(self.value)
        info.append(line)
        return info

    def hit(self, damage):
        self.health -= damage

    def get_value(self):
        return self.value

    def set_destinations(self, destinations):
        self.destinations = destinations
        
    def has_destination(self):
        return self.visited < len(self.destinations)

    def is_dead(self):
        return self.health <= 0

    #-Movimenta o mob pelo caminho premeditado
    def move(self):
        #-Calcula os passos a serem dados, speed*framerate
        steps = self.speed*self.dt
        while steps > 0 and self.has_destination():
            x, y = self.position
            destination = self.destinations[self.visited]
            if self.position == destination:
                self.visited += 1
                continue
            sign_x = -1
            if destination[0] > x:
                sign_x = 1
            elif destination[0] == x:
                sign_x = 0
            sign_y = -1
            if destination[1] > y:
                sign_y = 1
            elif destination[1] == y:
                sign_y = 0

            x += sign_x
            y += sign_y
            self.position = (x, y)
            steps -= 1

    #-Magia que mantem as atualizacoes na movimentacao dos mob
    def game_magic(self, mouse_pos, newclicks):
        t = time.time()
        self.dt = t - self.last_frame
        self.last_frame = t

        self.healthbar.update_health(self.health)
        self.follow_mob_pos()
        
        actions = []
        #-Se clicar no Mob, salva a acao
        if 1 in newclicks:
            if self.is_inside(mouse_pos):
                actions.append((13, self))
        #-Se o Mob morrer, salva a acao
        if self.health <= 0:
            actions.append((12, self))
        self.move()
        self.speed_modifier = 1
        return actions

#-Variacoes de Mobs
class EasyMob(Mob):
    ident = "trabalho"
    def __init__(self, position):
        Mob.__init__(self, position, 100, "Trabalho", 75, "files/mob.png", 25)

class MediunMob(Mob):
    ident = "prova"
    def __init__(self, position):
        Mob.__init__(self, position, 500, "Prova", 60, "files/mob2.png", 150)

class HardMob(Mob):
    ident = "final"
    def __init__(self, position):
        Mob.__init__(self, position, 2000, "Final", 50, "files/mob3.png", 500)
