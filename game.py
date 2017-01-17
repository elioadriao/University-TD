# -*- coding: latin1 -*-
#-Helio A. Adriao dos Santos-#
#----------------------------#

import pygame
import pygame.locals
import mob
import map
import tower
import menu
import button
import display
import alert
from os import path

#-Classe principal do jogo
class Game():
    def __init__(self):
        #-Inicia a tela do jogo com altura e largura fixa
        self.width = 590
        self.height = 695
        self.on = True
        self.quit = False
        self.name = "Universidade TD"
        pygame.font.init()
        self.font = pygame.font.SysFont("sans", 16)
        self.font_color = (0, 0, 0)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.locals.DOUBLEBUF | pygame.locals.SRCALPHA)
        pygame.display.set_caption(self.name)
        self.img_logo = pygame.image.load("files/logo.png")
        self.img_level = pygame.image.load("files/level_select.png")

        #-Inicia Menus do Jogo
        self.menu_a = menu.Menu((7, 538), 120, 50)  #-Compra de torres
        self.menu_b = menu.Menu((132, 538), 130, 50)#-Botoes de torres
        self.menu_c = menu.Menu((7, 593), 255, 77)  #-Botoes de progresso
        self.display = display.Display()            #-Display de informacoes
        self.menu_ini = menu.Menu((5, 615), 580, 75)#-Menu Principal
        self.ls_menu = menu.Menu((5, 115), 580, 495)#-Menu de Level

        #-Define variacoes de objetos
        self.tower_types = [tower.FastTower, tower.LightTower, tower.HeavyTower]
        self.mob_types = [mob.EasyMob, mob.MediunMob, mob.HardMob]

        #-Adciona os botoes aos menus
        for btn in [button.Play, button.Quit]:
            self.menu_ini.add_button(btn)
        self.menu_ini.center_x()

        for btn in [button.Upgrade, button.Sell]:
            self.menu_b.add_button(btn)
        self.menu_b.center_x()

        for btn in [button.NewWave, button.Quit]:
            self.menu_c.add_button(btn)
        self.menu_c.center_x()

        for lv in [button.Level, button.Level2, button.Level3, button.Level4]:
            self.ls_menu.add_level(lv)

        for t in self.tower_types:
            self.menu_a.add_purchaser(t)

        #-Inicializa os alertas e zera as variaveis
        self.alerts = set()
        self.empty_data()

    #-Retorna de 1 a 3, dependendo do tipo de mob, 0 se nao achar
    def get_mob_id(self, identifier):
        for i in range(len(self.mob_types)):
            if identifier == self.mob_types[i].ident:
                return i
        return 0

    #-Carrega o level, numero de vidas, dinheiro e mobs e o mapa
    def load_level(self, level):
        self.world = map.Map(level)
        self.tower_types = []
        self.money = 1000
        self.wave = 0
        self.wave_comp = 0
        self.waves = [None]
        self.lives = 5
        self.mobs = set()
        self.state = 22
        self.sub_state = 14
        self.purchaser_object = None
        self.purchaser = None
        self.selected = None
        self.selected_rect = pygame.rect.Rect((0, 0), (0, 0))
        self.selected_rect_set = False
        self.display.deactivate()
        self.alerts = set()
        #self.alert_life_lost_pos = (250, 5)

        #-Abre o Aquivo, salva em fin
        f = open(level, 'rb')
        fin = [line.strip() for line in f.readlines()]
        f.close()
        
        #-Puxa dados do arquivo
        self.money = float(fin[0])
        self.lives = int(fin[1])
        num_waves = int(fin[2])

        #-Recorta o arquivo para ler apenas os mob
        fin = fin[3:num_waves+3]
        for line in fin:
            #-3 tipos de mob, 0 unidades
            wave = [0, 0, 0]
            line = line.split()
            #-Se o id encontrado no arquivo for existente: mob++
            for identifier in line:
                mob_id = self.get_mob_id(identifier)
                wave[mob_id] += 1
            self.waves.append(wave)

    #-Zera as variaveis
    def empty_data(self):
        self.world = None
        self.tower_types = []
        self.money = 0
        self.wave = 0
        self.waves_comp = 0
        self.lives = 0
        self.mobs = set()
        self.state = 17
        self.sub_state = 14
        self.purchaser_object = None
        self.purchaser = None
        self.selected = None
        self.selected_rect = pygame.rect.Rect((0, 0), (0, 0))
        self.selected_rect_set = False
        self.display.deactivate()
        self.alerts = set()
        self.alert_life_lost_pos = (0, 0)
        self.waves = [None]

    #-Retorna se a atual acabou e se restam ondas
    def can_start_wave(self):
        return self.state == 22 and self.wave+1 <= len(self.waves)-1

    #-Desenha todas as telas do jogo
    def draw_this(self, surface):
        surface.fill((200, 200, 200))

        #-Se a acao for Menu
        if self.state == 17:
            surface.blit(self.img_logo, (0, 0))
            self.menu_ini.draw_this(surface)

        #-Se a acao for Level
        elif self.state == 18:
            self.menu_ini.draw_this(surface)
            surface.blit(self.img_level, (5, 5))
            self.ls_menu.draw_this(surface)

        #-Se nao, desenha o resto do jogo
        else:
            self.world.draw_this(surface)

            #-Desenha menus e balas
            for t in self.tower_types:
                t.draw_bullets(surface)
            self.menu_a.draw_this(surface)
            self.menu_b.draw_this(surface)
            self.menu_c.draw_this(surface)
            self.display.draw_this(surface)

            bag = "Valor da Bolsa: $%s" %(self.money)
            temp_surface = self.font.render(bag, 1, self.font_color)
            surface.blit(temp_surface, (5, 675))

            lives = "Chances Restantes: %d" %(self.lives)
            temp_surface = self.font.render(lives, 1, self.font_color)
            surface.blit(temp_surface, (222, 675))

            wave = "Periodo: %d" %(self.waves_comp+1)
            temp_surface = self.font.render(wave, 1, self.font_color)
            surface.blit(temp_surface, (444, 675))

            #-Desenha mob e barra de vida
            for mob in self.mobs:
                mob.draw_this(surface)
                mob.draw_life(surface)

            #-Desenha torres compradas, se existir
            if self.sub_state == 15:
                if self.purchaser_object is not None:
                    self.purchaser_object.draw_this(surface)

            #-Desenha as torres
            for tower in self.tower_types:
                if self.selected != tower:
                    tower.draw_this(surface)

            #-Desenha item selecionado
            if self.selected is not None:
                self.selected.draw_this(surface)

        #-Desenha os alertas
        for alert in self.alerts:
            alert.draw_this(surface)

    #-Inicializa a onda
    def begin_wave(self):
        if not self.can_start_wave():
            return
        self.wave += 1

        #-Cria os mobs, baseado na onda
        x, y = self.world.get_start()
        wave = self.waves[self.wave]
        for i in range(3):
            for j in range(wave[i]):
                c = self.mob_types[i]((0, 0))
                x -= 31
                c.set_position((x, y))
                destinations = [self.world.get_start()] + self.world.get_waypoints()
                c.set_destinations(destinations)
                self.mobs.add(c)
        
        self.state = 21

    #-Mostra item no display
    def display_item(self, item):
        self.display.deactivate()
        self.display.set_image(item.get_image(), item.get_width(), item.get_height())
        self.display.add_data(item.get_info())
        self.display.activate()

    #-Parte logica do jogo
    def game_magic(self, mouse_pos, newclicks):
        alerts_actions = []
        #-Converte os alerts em acoes
        for a in self.alerts:
            alert_actions = a.game_magic(mouse_pos, newclicks)
            for action in alert_actions:
                if action is not None:
                    alerts_actions.append(action)
        for action in alerts_actions:
            if action[0] == 39:
                self.alerts.remove(action[1])

        #-Coleta e ativa acoes do menu inicial
        if self.state == 17:
            actions = []
            mm_actions = self.menu_ini.game_magic(mouse_pos, newclicks)
            for action in mm_actions:
                if action is not None:
                    actions.append(action)

            for action in actions:
                if action[0] == 28:
                    self.state = 18
                elif action[0] == 29:
                    self.quit = True
                    return

        #-Coleta e ativa acoes do menu level
        elif self.state == 18:
            actions = []
            mm_actions = self.menu_ini.game_magic(mouse_pos, newclicks)
            for action in mm_actions:
                if action is not None:
                    actions.append(action)
            ls_actions = self.ls_menu.game_magic(mouse_pos, newclicks)
            #-Coleta level clicado
            for action in ls_actions:
                if action is not None:
                    actions.append(action)
            for action in actions:
                if action[0] == 29:
                    self.state = 17
                    return
                #-Carrega level clicado
                elif action[0] == 31:
                    self.load_level(action[1])

        #-Deixa o jogo em standby, clicou volta pro inicio
        elif self.state == 23 or self.state == 24:
            if 1 in newclicks:
                self.empty_data()

        #-Mensagem de final de level
        elif self.state == 22 and not self.can_start_wave():
            self.state = 24
            self.alerts.add(alert.Alert((95, 240), 400, 25, "Parabens! Voce Concluiu o Curso!"))

        #-Se nao, jogo continua
        else:
            #-Mensagem de Falha
            if self.lives <= 0:
                self.state = 23
                self.alerts.add(alert.Alert((95, 240), 400, 25, "Ah! Voce nao Consegiu, Tente Denovo"))
            #-Mensagem de fim de onda
            if self.state == 21 and len(self.mobs) == 0:
                self.waves_comp += 1
                message = "Voce Passou do %d Periodo!"%(self.waves_comp)
                self.alerts.add(alert.Alert((95, 215), 400, 25, message, True, 1))
                self.state = 22
            
            #-Mostra item selecionado no display
            if self.selected is not None:
                self.display_item(self.selected)

            #-Se clique direito precionado:
            if 3 in newclicks:
                if self.sub_state == 15:
                    self.purchaser_object.deactivate()
                    self.purchaser_object = None
                    self.selected = None
                    self.sub_state = 14
                    pygame.mouse.set_visible(True)
                    self.display.deactivate()
                #-Desativa alcance da torre e info
                elif self.sub_state == 16:
                    if self.selected.get_type() == 33 and self.selected != None:
                        self.selected.deactivate()
                        self.selected = None
                        self.sub_state = 14
                        self.display.deactivate()

            #-Mensagem de perca de chance
            for m in self.mobs:
                if not m.has_destination():
                    self.lives -= 1
                    if self.lives <= 0:
                        self.lives = 0
                    m.health = 0
                    message = "Voce Perdeu essa Chance! So restam %d."%(self.lives)
                    self.alerts.add(alert.Alert((250, 5), 350, 25, message, True, 1))

            #-Posiciona a torre nas coord do mouse
            if self.sub_state == 15:
                self.purchaser_object.set_position(mouse_pos)

            actions = []
            actions_placing = []
            #-Coleta acoes dos menus, filtra e salva
            menu_actions = self.menu_a.game_magic(mouse_pos, newclicks)
            for action in menu_actions:
                if action is not None:
                    if action[0] == 6:
                        actions_placing.append(action)
                    else:
                        actions.append(action)

            b_menu_actions = self.menu_c.game_magic(mouse_pos, newclicks)
            for action in b_menu_actions:
                if action is not None:
                    actions.append(action)

            c_menu_actions = self.menu_b.game_magic(mouse_pos, newclicks)
            for action in c_menu_actions:
                if action is not None:
                    actions.append(action)

            #-coleta acoes nas torres
            for tower in self.tower_types:
                tower_actions = tower.game_magic(mouse_pos, newclicks, self.mobs)
                for action in tower_actions:
                    if action is not None:
                        actions.append(action)
            #-Coleta acoes nos mob
            for m in self.mobs:
                creep_actions = m.game_magic(mouse_pos, newclicks)
                for action in creep_actions:
                    if action is not None:
                        actions.append(action)

            #-Mantem o cursor off no posicionamento de torre
            if self.sub_state != 15:
                pygame.mouse.set_visible(True)
            
            #-Executa as acoes de compra
            for action in actions_placing:
                if self.purchaser_object is None:
                        break
                placed = False
                #-Se clicado em torre no menu compra
                if self.purchaser_object.type == 33:
                    t_size = self.purchaser_object.get_size()
                    cell_num = self.world.get_cell_at(mouse_pos)
                    #-Se local existe no mapa, se dinheiro suficiente, se cabe no local, posiciona a torre
                    if self.world.has_cell(cell_num):
                        if self.purchaser_object.get_cost() <= self.money:
                            if self.world.can_build_tower(mouse_pos, t_size):
                                self.world.occupy_area(mouse_pos, t_size)
                                self.purchaser_object.activate()
                                self.tower_types.append(self.purchaser_object)
                                self.money -= self.purchaser_object.get_cost()
                                self.selected = self.purchaser_object
                                self.sub_state = 16
                                self.display_item(self.selected)
                                placed = True
                if not placed:
                    self.sub_state = 14
                    self.display.deactivate()

            #-Executa acoes coletadas
            for action in actions:
                if action[0] == 5:
                    #-Acao de compra de torre
                    if self.sub_state == 16:
                        if self.selected is not None and self.selected.get_type() == 33:
                            self.selected.deactivate()
                        self.display.deactivate()
                        self.selected = None
                    self.sub_state = 15
                    self.purchaser = action[1][0]
                    self.purchaser_object = action[1][1]
                    self.purchaser_object.activate()
                    pygame.mouse.set_visible(False)
                    self.display_item(self.purchaser_object)

                elif action[0] == 7:
                    #-Acao de hover do mouse
                    x, y = action[1].get_position()

                    message = action[1].get_hover_message()
                    a = alert.Alert((x, 415), 140, 125, message, True, .1)
                    self.alerts.add(a)

                elif action[0] == 8:
                    #-Acao de clique em outra torre
                    if self.sub_state == 15:
                        self.purchaser_object = None
                    if self.selected is not None and self.selected.get_type() == 33:
                        self.selected.deactivate()
                    self.selected = None
                    self.selected = action[1]
                    self.selected.activate()
                    self.display_item(self.selected)
                    self.sub_state = 16
                    self.display_item(self.selected)

                elif action[0] == 13:
                    #-Acao de clique em mob
                    self.selected = action[1]
                    self.sub_state = 16
                    self.display_item(self.selected)

                elif action[0] == 12:
                    #-Acao de mob morto
                    if action[1] == self.selected:
                        self.display.deactivate()
                        self.selected = None
                        self.sub_state = 14
                    self.money += action[1].get_value()
                    self.mobs.remove(action[1])

                elif action[0] == 25:
                    #-Acao de comecar onda
                    self.begin_wave()

                elif action[0] == 26:
                    #-Acao de melhoria de torre
                    if self.sub_state == 16:
                        if self.selected is not None and self.selected.type == 33:
                            if self.selected.can_be_upgraded():
                                cost = self.selected.get_upgrade_cost()
                                if self.money >= cost:
                                    self.selected.upgrade()
                                    self.money -= cost
                                    self.display_item(self.selected)

                elif action[0] == 27:
                    #-Acao de venda de torre
                    if self.sub_state == 16:
                        if self.selected is not None and self.selected.type == 33:
                            self.money += self.selected.get_sell_amount()
                            self.world.free_area(self.selected.get_position(), self.selected.get_size())
                            for i in range(len(self.tower_types)):
                                if self.tower_types[i].get_position() == self.selected.get_position():
                                    self.tower_types.pop(i)
                                    break
                            self.selected = None
                            self.sub_state = 14
                            self.display.deactivate()

                elif action[0] == 29:
                    #-Acao de sair
                    self.empty_data()
                    
            #-Se a torre pode ser posicionada, range verde, senao vermelho
            if self.purchaser_object is not None:
                if self.purchaser_object.type == 33:
                    if not self.world.can_build_tower(self.purchaser_object.get_position(), self.purchaser_object.get_size()):
                        self.purchaser_object.bad_pos()
                    else:
                        self.purchaser_object.good_pos()
    #-Funcao que inicia o loop do pygame
    def start(self):
        clock = pygame.time.Clock()
        mouse_pos = (0, 0)
        while True :
            clock.tick(30)
            newclicks = set()

            for e in pygame.event.get():
                #-Fecha o jogo se clicar em exit
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return

                #-Coleta os clicks do mouse
                if e.type == pygame.MOUSEBUTTONUP:
                    newclicks.add(e.button)

                #-Coleta a posxy do mouse
                if e.type == pygame.MOUSEMOTION:
                    mouse_pos = e.pos

            if self.on:
                self.game_magic(mouse_pos, newclicks)
                if self.quit == True:
                    pygame.quit()
                    return
                self.draw_this(self.screen)
            # -Se o jogo tiver aberto tudo certo, desenha a tela
            pygame.display.flip()
