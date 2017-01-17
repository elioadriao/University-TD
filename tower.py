# -*- coding: latin1 -*-
#-Helio A. Adriao dos Santos-#
#----------------------------#

import pygame
import rectangle
import math
import bullet
import time

class Tower(rectangle.Rectangle):
    def __init__(self, position, width, height, image, name, rng, cost, atk_speed):
        rectangle.Rectangle.__init__(self, 33, position, width, height, image)
        self.cost = cost
        self.range = rng
        self.active = False
        self.level = 0
        self.bullet_damage = [25, 50, 100, 200]
        self.atk_speed = atk_speed
        self.last_attack = self.atk_speed[self.level]
        self.is_good = False

        #-Calcula a range e gera a sombra verde
        self.range_surface_good = pygame.Surface((self.range[self.level]*2, self.range[self.level]*2), pygame.SRCALPHA)
        self.range_surface_bad = pygame.Surface((self.range[self.level]*2, self.range[self.level]*2), pygame.SRCALPHA)
        self.generate_range()

        self.bullet_type = bullet.Bullet
        self.target = None
        self.bullets = set()
        self.name = name

    def can_be_upgraded(self):
        return self.level+1 < len(self.cost)

    #-Retorna o valor de upgrade da lista cost
    def get_upgrade_cost(self):
        if self.can_be_upgraded():
            return self.cost[self.level+1]
        else:
            return 0

    def get_total_cost(self):
        total_cost = 0
        for i in range(self.level+1):
            total_cost += self.cost[i]
        return total_cost

    def get_sell_amount(self):
        rounded = "%.2f" %(self.get_total_cost()*0.5)
        return float(rounded)

    def upgrade(self):
        if self.can_be_upgraded():
            self.level += 1
            #-Atualiza a range da torre
            self.range_surface_good = pygame.Surface((self.range[self.level]*2, self.range[self.level]*2), pygame.SRCALPHA)
            self.range_surface_bad = pygame.Surface((self.range[self.level]*2, self.range[self.level]*2), pygame.SRCALPHA)
            self.generate_range()

    def get_hover_message(self):
        message = ""
        message += "%s" %(self.name)
        message += "\nDano: %.1f" %(self.bullet_damage[self.level])
        message += "\nArea: %.1f" %(self.range[self.level])
        message += "\nVelocidade: %.1f/s" %(self.atk_speed[self.level])
        message += "\nPreco: $%.2f" %(self.cost[self.level])
        return message

    def get_info(self):
        info = []
        line = "%s" %(self.name)
        info.append(line)
        line = "Nivel: %d" %(self.level+1)
        info.append(line)

        #-Filtro para mostrar upgrade quando disponivel
        if not self.can_be_upgraded():
            line = "Dano: %.1f" %(self.bullet_damage[self.level])
            info.append(line)
            line = "Area: %.1f" %(self.range[self.level])
            info.append(line)
            line = "Velocidade: %.1f/s" %(self.atk_speed[self.level])
            info.append(line)
            line = "Valor de Melhoria: Maximo"
            info.append(line)
        else:
            line = "Dano: %.1f > [%.1f]" %(self.bullet_damage[self.level], self.bullet_damage[self.level+1])
            info.append(line)
            line = "Area: %.1f > [%.1f]" %(self.range[self.level], self.range[self.level+1])
            info.append(line)
            line = "Velocidade: %.1f/s (->%.1f)" %(self.atk_speed[self.level], self.atk_speed[self.level+1])
            info.append(line)
            line = "Valor de Melhoria: $%.1f" %(self.cost[self.level+1])
            info.append(line)
        line = "Valor Venda: $%.2f" %(self.get_sell_amount())
        info.append(line)
        return info

    def get_cost(self):
        return self.cost[self.level]
        
    def is_active(self):
        return self.active
        
    def activate(self):
        self.active = True
        
    def deactivate(self):
        self.active = False
        
    def is_in_range(self, position):
        px, py = position
        cx, cy = self.get_center()
        distance = math.sqrt((px-cx)**2 + (py-cy)**2)
        return distance <= self.range[self.level]

    def generate_range(self, color_good=(50, 255, 50, 125), color_bad=(255, 50, 50, 125)):
        self.range_surface_good.fill((255, 255, 255, 0))
        self.range_surface_bad.fill((255, 255, 255, 0))
        #-Gera um circulo verde e vermelho
        cx, cy = self.get_center()
        topleft = (cx - self.range[self.level], cy - self.range[self.level])
        for i in range(self.range_surface_good.get_width()):
            for j in range(self.range_surface_good.get_height()):
                if self.is_in_range((i + topleft[0], j + topleft[1])):
                    self.range_surface_good.set_at((i, j), color_good)
                    self.range_surface_bad.set_at((i, j), color_bad)

    def bad_pos(self):
        if self.is_good:
            self.is_good = False

    def good_pos(self):
        if not self.is_good:
            self.is_good = True
        
    def draw_range(self, surface):
        if self.is_active():
            #-Desenha a area, verde se is_good, vermelho senao
            cx, cy = self.get_center()
            topleft = (cx - self.range[self.level], cy - self.range[self.level])
            if self.is_good:
                surface.blit(self.range_surface_good, topleft)
            else:
                surface.blit(self.range_surface_bad, topleft)
                
    def can_attack(self):
        return time.time() - self.last_attack >= 1.0/self.atk_speed[self.level]

    #-Inicia o ataque ao alvo
    def attack(self, target):
        b = self.bullet_type(self.get_center(), self.bullet_damage[self.level])
        b.set_target(target)
        self.bullets.add(b)
        self.last_attack = time.time()
     
    def draw_this(self, surface):
        if self.is_active():
            self.draw_range(surface)
        surface.blit(self.image, self.position)

    def draw_bullets(self, surface):
        for bullet in self.bullets:
            bullet.draw_this(surface)
        
    def game_magic(self, mouse_pos, newclicks, mobs):
        #-Limpa o alvo
        if self.target is not None and self.target.is_dead():
            self.target = None

        #-Inicia e captura as acoes das balas
        bullets_actions = []
        for bullet in self.bullets:
            bullet_actions = bullet.game_magic(mouse_pos, newclicks)
            for a in bullet_actions:
                if a is not None:
                    bullets_actions.append(a)
        #-Dentro das acoes das balas, captura as acoes de fim(10) e morte(11) do alvo
        actions = []
        for action in bullets_actions:
            if action[0] == 10:
                self.bullets.remove(action[1])
            if action[0] == 11:
                actions.append(action)
        
        if self.is_inside(mouse_pos):
            if 1 in newclicks:
                actions.append((8, self))

        #-Ataca o alvo se dentro da area, senao, procura na lista de alvos o proximo
        if self.can_attack():
            if self.target is not None and self.is_in_range(self.target.get_center()):
                self.attack(self.target)
            else:
                for mob in mobs:
                    if self.is_in_range(mob.get_center()):
                        self.target = mob
                        self.attack(mob)
                        self.fs_last_attack = 0
                        break
        return actions

#-Variacoes de torre
class FastTower(Tower):
    def __init__(self, position):
        Tower.__init__(self, position, 16, 16, "files/torre2.png", "Livro", [50, 60, 70, 80], [50, 100, 200, 400], [6, 6, 7, 8])
        self.bullet_type = bullet.Bullet
        self.bullet_damage = [16, 32, 64, 128]

class LightTower(Tower):
    def __init__(self, position):
        Tower.__init__(self, position, 32, 32, "files/torre.png", "Novato", [70, 80, 90, 100], [75, 150, 250, 400], [2, 2.5, 3, 3])
        self.bullet_type = bullet.Bullet
        self.bullet_damage = [25, 50, 75, 100]

class HeavyTower(Tower):
    def __init__(self, position):
        Tower.__init__(self, position, 32, 32, "files/torre3.png", "Veterano", [100, 125, 150, 200], [200, 400, 800, 1200], [1, 2, 2, 2])
        self.bullet_type = bullet.Bullet
        self.bullet_damage = [150, 250, 350, 750]
