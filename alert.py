# -*- coding: latin1 -*-
#-Helio A. Adriao dos Santos-#
#----------------------------#

import pygame
import time

class Alert():
    def __init__(self, position, width, height, message, expires = False, duration = 3, font = "sans", font_size = 16, font_color = (0, 0, 0), margin_x = 5, margin_y = 5, bg_color = (200, 200, 200), b_color = (100, 100, 100)):
        #Inicia a a classe alert define os padroes, formata a mensagem e inicia o timeout
        self.position = position
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(font, font_size)
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.format_message(message)
        self.font_color = font_color
        self.bg_color = bg_color
        self.o_color = b_color
        self.expires = expires
        self.duration = duration
        self.start = time.time()

    def format_message(self, message):
        # Divide a mensagem em linhas baseadas no tamanho do campo (width)
        messages = [message]
        width = self.width - 2*self.margin_x

        while self.font.size(messages[-1])[0] > width:
            m1 = ""
            m2 = messages[-1]

            while True:
                word = ""
                while not m2[0].isspace():
                    word += m2[0]
                    m2 = m2[1:]
                    if len(m2) == 0:
                        break
                cand = m1 + ' ' + word
                if self.font.size(cand.strip())[0] <= width:
                    m1 = cand.strip()
                    if m2[0] == '\n':
                        m2 = m2.strip()
                        break
                    else:
                        m2 = m2.strip()
                else:
                    m2 = word + m2
                    break
            messages[-1] = m1
            if len(m2) > 0:
                messages.append(m2)
        self.messages = messages

        message_sizes = []
        for message in self.messages:
            message_sizes.append(self.font.size(message))
        self.message_sizes = message_sizes

        message_positions = []
        y = self.margin_y
        for i in range(len(self.messages)):
            x = (self.width - self.message_sizes[i][0])*.5
            message_positions.append((x, y))
            y += self.margin_y + self.message_sizes[i][1]
        self.message_positions = message_positions

    def game_magic(self, mouse_pos, newclicks, ):
        # Sobrescreve a magia do jogo para executar o timeout da mensagem
        actions = []
        if self.expires and time.time() - self.start >= self.duration:
            actions.append((39, self))
        return actions

    def set_bg_color(self, bg_color):
        self.bg_color = bg_color

    def set_o_color(self, o_color):
        self.o_color = o_color

    def set_font(self, font, font_size):
        self.font = pygame.font.SysFont(font, font_size)

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message

    def calc_center(self):
        px, py = self.position
        cx, cy = px + .5*self.width, py + .5*self.height
        return (int(cx), int(cy))

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position
        self.calc_center

    def get_center(self):
        return self.calc_center()

    def get_width(self):
        return self.width

    def set_width(self, width):
        self.width = width
        self.calc_center

    def get_height(self):
        return self.height

    def set_height(self, height):
        self.height = height
        self.cacl_center

    def get_dims(self):
        return (self.get_width(), self.get_height())
    
    def draw_this(self, surface):
        # Desenha o campo e a mensagem
        a_surface = pygame.Surface((self.width, self.height))
        a_surface.fill(self.bg_color)

        r = pygame.Rect((0, 0), (self.width, self.height))
        pygame.draw.rect(a_surface, self.o_color, r, 3)

        for i in range(len(self.messages)):
            temp_surface = self.font.render(self.messages[i], 1, self.font_color)
            a_surface.blit(temp_surface, self.message_positions[i])

        surface.blit(a_surface, self.position)

    def is_inside(self, position):
        if position[0] >= self.position[0] and position[0] < self.position[0] + self.width:
            if position[1] >= self.position[1] and position[1] < self.position[1] + self.height:
                return True
        return False
