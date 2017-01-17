# -*- coding: latin1 -*-
#-Helio A. Adriao dos Santos-#
#----------------------------#

import pygame
import rectangle

class Display(rectangle.Rectangle):
    def __init__(self):
        #-inicia o menu display
        self.position = (265, 538)
        self.width = 318
        self.height = 132
        self.color_bg = (200, 200, 200)
        self.color_border = (100, 100, 100)
        self.data = []
        self.active = False
        self.margin_x = 5
        self.margin_y = 5

        self.item_image = None
        self.item_image_x = self.margin_x
        self.item_image_y = 0
        self.data_x = self.width/3

        self.font = pygame.font.SysFont("sans", 14)
        self.font_height = self.font.get_height()
        self.font_color = (0, 0, 0)

    #-Adiciona data ao display e adiciona altura dos dados
    def add_data(self, data):
        for datum in data:
            self.data.append(datum)
            self.data_ys.append(self.margin_y + (len(self.data) - 1) * self.font_height)

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
        self.item_image = None
        self.data = []
        self.data_ys = []

    def set_image(self, image, width, height):
        self.item_image = image
        self.item_image_y = (self.height - height)/2
        self.item_image_x = (self.data_x - width)/2

    #-Desenha o Display
    def draw_this(self, surface):
        d_surface = pygame.Surface((self.width, self.height))
        d_surface.fill(self.color_bg)
        
        r = pygame.Rect((0, 0), (self.width, self.height))
        pygame.draw.rect(d_surface, self.color_border, r, 3)

        #-Se Ativado desenha a imagen do item e os status
        if self.active:
            d_surface.blit(self.item_image, (self.item_image_x, self.item_image_y))

            for i in range(len(self.data)):
                temp_surface = self.font.render(self.data[i], 1, self.font_color)
                d_surface.blit(temp_surface, (self.data_x, self.data_ys[i]))

        surface.blit(d_surface, self.position)
