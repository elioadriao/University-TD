# -*- coding: latin1 -*-
#-Helio A. Adriao dos Santos-#
#----------------------------#

import rectangle
import os

class Map:
    def __init__(self, layout_file=None):
        self.position = (7, 5)
        self.width = 576
        self.height = 528
        self.cell_width = 16
        self.cell_height = 16
        self.occupied_locations = []
        self.layout = []
        self.tile_types = []
        self.waypoints = []
        self.start_cell = None
        if layout_file is not None:
            self.load_file(layout_file)
        self.start = self.get_cell_top_left(self.get_cell_num(self.start_cell[0], self.start_cell[1]))
        self.order_waypoints()

    def get_position(self):
        return self.position

    def get_dims(self):
        return (self.width, self.height)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_waypoints(self):
        return self.waypoints

    #-Carrega o Mapa pelo arquivo .txt
    def load_file(self, layout_file):
        if not os.path.exists(layout_file):
            print "Error404"
            return

        f = open(layout_file, 'rb')
        fin = [line.strip() for line in f.readlines()]
        f.close()

        #-Pula ate o inicio do mapa dentro do arquivo
        fin = fin[2:]
        skip = int(fin[0])
        fin = fin[skip+1:]
        data = fin[0].split()
        dim = [0, 0]
        #-Tenta Carregar o mapa, e salvar as linhas no layout
        try:
            dim[0] = int(data[0])
            dim[1] = int(data[1])
            self.start_cell = (int(data[2]), int(data[3]))

            layout = []
            fin = fin[1:]
            for line in fin:
                layout.append(line)
        except Exception, e:
            print e
            return False

        #-Faz a matriz do mapa ja definindo onde e caminho ou nao
        self.layout = []
        waypoints = []
        for j in range(len(layout)):
            r_row = []
            t_row = []
            t_locations = []
            for i in range(len(layout[j])):
                tile = layout[j][i]
                if tile == str(0):
                    img = "files/grock.png"
                else:
                    img = "files/gpath.png"
                    if tile == str(3):
                        waypoints.append((i, j))
                x = self.position[0] + (i)*self.cell_width
                y = self.position[1] + (j)*self.cell_height
                t_row.append(int(tile))
                t_locations.append(0)
                r_row.append(rectangle.Rectangle(35, (x, y), self.cell_width, self.cell_height, img))

            self.layout.append(r_row)
            self.tile_types.append(t_row)
            self.occupied_locations.append(t_locations)
        for point in waypoints:
            self.waypoints.append(self.get_cell_top_left(self.get_cell_num(point[0], point[1])))
        return True

    #-Verifica se o waypoint é no centro
    def is_center(self, i, j):
        if self.tile_types[j][i] == 3:
            return True
        can_top = j > 0
        can_left = i > 0
        can_right = i < self.width - 1
        can_bottom = j < self.height - 1
        if can_top:
            if not self.is_path(self.get_cell_num(i, j-1)):
                return False
            if can_left:
                if not self.is_path(self.get_cell_num(i-1, j-1)):
                    return False
            if can_right:
                if not self.is_path(self.get_cell_num(i+1, j-1)):
                    return False
        else:
            return False
        if not can_left or not self.is_path(self.get_cell_num(i-1, j)):
            return False
        if not can_right or not self.is_path(self.get_cell_num(i+1, j)):
            return False
        if can_bottom:
            if not self.is_path(self.get_cell_num(i, j+1)):
                return False
            if can_left:
                if not self.is_path(self.get_cell_num(i-1, j+1)):
                    return False
            if can_right:
                if not self.is_path(self.get_cell_num(i+1, j+1)):
                    return False
        else:
            return False
        return True

    #-Define a direcao da tragetoria procurando por waypoints nas direcoes
    def get_path(self, i, j):
        path = []
        can_top = j > 0
        can_left = i > 0
        can_right = i < self.width - 1
        can_bottom = j < self.height - 1
        if can_top and self.is_center(i, j-1):
            path.append((i, j-1))
        if can_left and self.is_center(i-1, j):
            path.append((i-1, j))
        if can_right and self.is_center(i+1, j):
            path.append((i+1, j))
        if can_bottom and self.is_center(i, j+1):
            path.append((i, j+1))
        return path

    #-Define a sequencia dos waypoints
    def order_waypoints(self):
        ordered_waypoints = []
        i, j = self.start_cell
        count = 0
        end = len(self.waypoints)
        prev = []
        while count < end:
            next_prev = []
            path = self.get_path(i, j)
            for neighbor in path:
                if neighbor not in prev:
                    next_prev.append((i, j))
                    i, j = neighbor
                    if self.tile_types[j][i] == 3:
                        count += 1
                        ordered_waypoints.append(self.get_cell_top_left(self.get_cell_num(i, j)))
            prev = next_prev[:]
        self.waypoints = ordered_waypoints[:]
        
        last = self.waypoints[-1]
        p = self.get_cell_top_left(self.get_cell_num(prev[0][0], prev[0][1]))
        dx, dy = (last[0]-p[0], last[1]-p[1])
        end = (last[0]+dx*2, last[1]+dy*2)
        self.waypoints.append(end)

    def draw_this(self, surface):
        for row in self.layout:
            for cell in row:
                cell.draw_this(surface)

    def get_cell_at(self, position):
        for j in range(len(self.layout)):
            for i in range(len(self.layout[0])):
                if self.layout[j][i].is_inside(position):
                    return self.get_cell_num(i, j)
        return None
        
    def get_start(self):
        return self.start

    def get_end(self):
        return self.waypoints[-1]

    def get_cell_num(self, i, j):
        return j*(self.width/self.cell_width) + i

    def get_cell_posxy(self, cell_num):
        i = cell_num%(self.width/self.cell_width)
        j = cell_num/(self.width/self.cell_width)
        return i, j

    def get_cell_top_left(self, cell_num):
        i, j = self.get_cell_posxy(cell_num)
        return self.layout[j][i].get_position()

    def is_path(self, cell_num):
        i, j = self.get_cell_posxy(cell_num)
        return self.tile_types[j][i] == 2 or self.tile_types[j][i] == 3

    def occupy_cell(self, cell_num):
        i, j = self.get_cell_posxy(cell_num)
        self.occupied_locations[j][i] = 1

    def occupy_area(self, pos, dims):
        x_span = dims[0] / self.cell_width
        y_span = dims[1] / self.cell_height
        for i in range(x_span):
            for j in range(y_span):
                p = (pos[0] + i*self.cell_width, pos[1] + j*self.cell_height)
                cell_num = self.get_cell_at(p)
                self.occupy_cell(cell_num)

    def free_cell(self, cell_num):
        i, j = self.get_cell_posxy(cell_num)
        self.occupied_locations[j][i] = 0

    def free_area(self, pos, dims):
        x_span = dims[0] / self.cell_width
        y_span = dims[1] / self.cell_height
        for i in range(x_span):
            for j in range(y_span):
                p = (pos[0] + i*self.cell_width, pos[1] + j*self.cell_height)
                cell_num = self.get_cell_at(p)
                self.free_cell(cell_num)

    def has_cell(self, cell_num):
        if cell_num is None or cell_num >= (self.width/self.cell_width)*(self.height/self.cell_height):
            return False
        return True

    def is_occupied(self, cell_num):
        i, j = self.get_cell_posxy(cell_num)
        return self.occupied_locations[j][i] == 1

    def can_build_tower(self, pos, dims):
        x_span = dims[0] / self.cell_width
        y_span = dims[1] / self.cell_height
        for i in range(x_span):
            for j in range(y_span):
                p = (pos[0] + i*self.cell_width, pos[1] + j*self.cell_height)
                cell_num = self.get_cell_at(p)
                if not self.has_cell(cell_num) or self.is_path(cell_num) or self.is_occupied(cell_num):
                    return False
        return True

    def is_inside(self, position):
        if position[0] >= self.position[0] and position[0] < self.position[0] + self.width:
            if position[1] >= self.position[1] and position[1] < self.position[1] + self.height:
                return True
        return False

    def __str__(self):
        board = ""
        for row in self.layout:
            line = ""
            for cell in row:
                line += str(cell)
            board += line + '\n'
        return board