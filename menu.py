# -*- coding: latin1 -*-
#-Helio A. Adriao dos Santos-#
#----------------------------#

import rectangle
import purchaser
import pygame

class Menu(rectangle.Rectangle):
    def __init__(self, position, width, height, bg_color = (200, 200, 200), bo_color = (100, 100, 100)):
        self.position = position
        self.width = width
        self.height = height
        self.color_bg = bg_color
        self.color_border = bo_color
        self.items = []
        self.margin_x = 10
        self.margin_y = 10

    def clear(self):
        self.items = []

    #-Calcula o a posxy do proximo item, baseado na lista de items declarados no menu
    def next_item_position(self, item):
        y = .5*(self.height - item.get_height())
        x = self.margin_x
        for item in self.items:
            x += item.get_width() + self.margin_x
        return (x, y)

    # Centraliza o menu na horizontal, baseado na width total/width usada
    def center_x(self):
        used_width = 0
        for item in self.items:
            used_width += item.get_width()
        used_width += (len(self.items)-1)*self.margin_x

        starting_x = (self.width-used_width)/2
        current_x = starting_x
        for item in self.items:
            x, y = item.get_position()
            x = current_x
            current_x += (item.get_width()+self.margin_x)
            item.set_position((x, y))

    #-Captura as acoes realizadas no menu
    def game_magic(self, mouse_pos, newclicks, ):
        mx, my = mouse_pos[0] - self.position[0], mouse_pos[1] - self.position[1]
        actions = []
        for item in self.items:
            item_actions = item.game_magic((mx, my), newclicks)
            for action in item_actions:
                if action is not None:
                    actions.append(action)
        return actions
        
    def add_button(self, buttontype):
        btn = buttontype()
        pos = self.next_item_position(btn)
        btn.set_position(pos)
        self.items.append(btn)

    def add_level(self, buttontype):
        btn = buttontype()
        self.items.append(btn)

    def add_purchaser(self, towertype):
        tower = towertype((0, 0))
        pos = self.next_item_position(tower)
        self.items.append(purchaser.Purchaser(pos, towertype, tower.get_width(), tower.get_height()))

    def draw_this(self, surface):
        m_surface = pygame.Surface((self.width, self.height))
        m_surface.fill(self.color_bg)

        r = pygame.Rect((0, 0), (self.width, self.height))
        pygame.draw.rect(m_surface, self.color_border, r, 3)
        for item in self.items:
            item.draw_this(m_surface)

        surface.blit(m_surface, self.position)
