# -*- coding: latin1 -*-
#-Helio A. Adriao dos Santos-#
#----------------------------#

import pygame
import rectangle

class Button(rectangle.Rectangle):
    def __init__(self, position, width, height, image, image_hover):
        rectangle.Rectangle.__init__(self, 36, position, width, height, image)
        #-Dados de hover do botao
        self.image_hover = pygame.image.load(image_hover)
        self.message = None
        self.hover = False
        self.description = ""
        #-Item executado no clique
        self.item = None

    def draw_this(self, surface):
        #-Se hover, muda imagem, senao normal
        if self.hover:
            surface.blit(self.image_hover, self.position)
        else:
            surface.blit(self.image, self.position)
        
    def game_magic(self, mouse_pos, newclicks):
        actions = []
        #-Captura se a posicao do mouse esta sobre botao
        if self.is_inside(mouse_pos):
            self.hover = True

            #-Captura clique no botao
            if 1 in newclicks:
                actions.append((self.message, self.item))
        else:
            self.hover = False
        return actions

#-Variacoes de botoes
class NewWave(Button):
    def __init__(self, position = (0, 0)):
        Button.__init__(self, position, 98, 60, "files/bonda.png", "files/bonda_hover.png")
        self.message = 25
        self.item = None

class Upgrade(Button):
    def __init__(self, position = (0, 0)):
        Button.__init__(self, position, 52, 32, "files/bupgrade.png", "files/bupgrade_hover.png")
        self.message = 26
        self.item = None

class Sell(Button):
    def __init__(self, position = (0, 0)):
        Button.__init__(self, position, 52, 32, "files/bsell.png", "files/bsell_hover.png")
        self.message = 27
        self.item = None

class Play(Button):
    def __init__(self, position = (0, 0)):
        Button.__init__(self, position, 98, 60, "files/bplay.png", "files/bplay_hover.png")
        self.message = 28
        self.item = None

class Quit(Button):
    def __init__(self, position = (0, 0)):
        Button.__init__(self, position, 98, 60, "files/bquit.png", "files/bquit_hover.png")
        self.message = 29
        self.item = None

class Level(Button):
    def __init__(self):
        Button.__init__(self, (45, 10), 240, 235, "files/l1.png", "files/l1_hover.png")
        self.message = 31
        self.item = "levels/world1.txt"

class Level2(Button):
    def __init__(self):
        Button.__init__(self, (295, 10), 240, 235, "files/l2.png", "files/l2_hover.png")
        self.message = 31
        self.item = "levels/world2.txt"

class Level3(Button):
    def __init__(self):
        Button.__init__(self, (45, 255), 240, 235, "files/l3.png", "files/l3_hover.png")
        self.message = 31
        self.item = "levels/world3.txt"

class Level4(Button):
    def __init__(self):
        Button.__init__(self, (295, 255), 240, 235, "files/l4.png", "files/l4_hover.png")
        self.message = 31
        self.item = "levels/world4.txt"
