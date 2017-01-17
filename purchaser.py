# -*- coding: latin1 -*-
#-Helio A. Adriao dos Santos-#
#----------------------------#

class Purchaser():
    def __init__(self, position, objtype, obj_width, obj_height):
        #-Inicia o Menu de compra de torres
        self.position = position
        self.objtype = objtype
        self.obj = objtype(position)
        self.status = 4
        self.width = obj_width
        self.height = obj_height
        
    def get_width(self):
        return self.width
        
    def get_height(self):
        return self.height
        
    def get_size(self):
        return (self.get_width(), self.get_height())

    def draw_this(self, surface):
        self.obj.draw_this(surface)

    def toggle_status(self):
        if self.status == 4:
            self.status = 5
        else:
            self.status = 4
            self.follower = None

    def game_magic(self, mouse_pos, newclicks):
        actions = []
        hover = self.obj.is_inside(mouse_pos)
        if hover:
            actions.append((7, self.obj))
        #-Click esquerdo
        if 1 in newclicks:
            if self.status == 4 and hover:
                #-Libera a torre para posicionamento
                actions.append((5, (self, self.objtype(self.position))))
                self.toggle_status()
            elif self.status == 5:
                #-Tenta fixa a torre no local
                actions.append((6, (self, self.objtype(self.position))))
                self.toggle_status()
        #-click direito: cancela a torre
        if 3 in newclicks:
            if self.status == 5:
                self.toggle_status()
        return actions
