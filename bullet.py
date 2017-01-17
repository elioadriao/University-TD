# -*- coding: latin1 -*-
#-Helio A. Adriao dos Santos-#
#----------------------------#

import rectangle
import math
import time

class Bullet(rectangle.Rectangle):
    def __init__(self, position, dmg=[25, 50, 100, 200]):
        rectangle.Rectangle.__init__(self, 37, position, 8, 8, "files/bullet.png")
        self.dmg = dmg
        self.speed = 300
        self.target = None

        self.last_frame = time.time()
        self.dt = 0

    def get_damage(self):
        return self.dmg

    def set_target(self, target):
        #
        self.target = target

    #-Movimenta o projetil em direcao ao centro do target
    def move(self):
        if self.target is None:
            return

        c_target = self.target.get_center()
        c_tower = self.get_center()
        
        direction = (c_target[0]-c_tower[0], c_target[1]-c_tower[1])
        x = direction[0]**2
        y = direction[1]**2

        #-Calcula o vetor do projetil
        mag = math.sqrt(float(x) + float(y))
        normalized = (direction[0]/mag, direction[1]/mag)

        distance = min(self.speed*self.dt, math.sqrt(x+y))
        self.position = (self.position[0] + distance*normalized[0], self.position[1] + distance*normalized[1])

    def game_magic(self, mouse_pos, newclicks):
        t = time.time()
        self.dt = t - self.last_frame
        self.last_frame = t

        self.move()

        actions = []
        #-Se o target some/morre manda o cod na action
        if self.target is None or self.target.is_dead():
            actions.append((10, self))
        #-Se a bala colide no target, seta o dano
        elif self.collide(self.target) or self.target.collide(self):
            self.target.hit(self.get_damage())
            if self.target.is_dead():
                actions.append((11, self.target.get_value()))
            actions.append((10, self))
        return actions
