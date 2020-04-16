# ==========================================
#
# Pygame Arkanoid
# Autor: manuel.mayo.lado@gmail.com
#
# ==========================================

from typing import Any, Tuple, Union

import pygame
import os

from pygame.font import FontType
from pygame.ftfont import Font
from pygame.surface import SurfaceType


class RectInfo:
    """
    Gestión del rectágulo de información.
    """
    def __init__(self, game, fase):
        """
        ::args
        :game: Clase Game
        :fase: Clase Fase
        """
        # Clase Game parent
        self.game = game
        # Clase Fase parent
        self.fase = fase
        # Color de fondo
        self.color_fondo = 205, 205, 200
        # Color fondo label 1
        self.color_fondo_label_1 = 205, 205, 200
        # Color fondo label 2
        self.color_fondo_label_2 = 221, 188, 149
        # Color letra títulos
        self.color_letra_titulos = 98, 109, 113
        # Color letra puntuaciones
        self.color_letra_puntuaciones = 98, 109, 113
        # directorio de los tipos de letras
        self.fonts_dir = self.game.config.fonts.dir
        # nombre del tipo de letra
        self.font_name = self.game.config.fonts.file
        # medidas del rectángulo de información
        self.rect = fase.rect_info
        # número de filas
        self.nfilas = 2
        # número de columnas
        self.ncolumnas = 2
        # medidas (px) del rectángulo de información
        self.rect_px = self.fase.ventana.game_px_2_window_px(self.rect)
        # old time
        self.seg_new_image = 0
        self.dec_new_image = 0
        # atributos que varian con el tamaño de la ventana
        self.set_surfaces()

    # self => None
    def set_surfaces(self):
        # espacio
        self.espacio = [self.rect_px[0] / 20, self.rect_px[1] / 20]
        # medidas del rectánculo label
        self.rect_label = [
            self.rect_px[0] / self.ncolumnas - self.espacio[0],
            self.rect_px[1] / self.nfilas - self.espacio[1]
            ]
        # tamaño de la letra
        self.font_size = int(self.rect_px[1] / 2.8)
        # tipo de letra y tamaño
        self.font_path = os.path.join(self.fonts_dir,self.font_name)
        if os.path.exists(self.font_path):
            self.font = pygame.font.Font(
                os.path.join(self.fonts_dir,self.font_name),
                self.font_size)
        else:
            self.font = pygame.font.SysFont(None,self.font_size)
        # pygame fondo surface
        self.fondo_img = self.crear_fondo()
        # pygame title vidas surface
        self.title_vidas_img = self.crear_title_vidas_img()
        # pygame time surface
        self.time_img = self.crear_time_img()
        # pygame title score surface
        self.title_score_img = self.crear_title_score_img()
        # pygame time surface
        self.fuel_img = self.crear_fuel_img()
        # pygame title score max
        self.title_score_total_img = self.crear_title_score_total_img()
        # pygame score max
        self.score_total_img = self.crear_score_total_img()
        # pygame imagen
        self.imagen = self.crear_imagen()
        # dibujar?
        self.actualizar_dibujo = 1

    # self, Fase => None
    def draw(self):
        #self.draw_fondo()
        self.draw_imagen()
        self.actualizar_dibujo = 0

    # self => None
    def draw_imagen(self):
       self.fase.surface.blit(self.imagen, (0,0))

    # self => None
    def draw_fondo(self):
        self.fase.surface.blit(self.fondo_img, (0,0))

    # self => None
    def draw_label(self, label, surface, pos):
        n_esp = [
            2-(1-1/self.ncolumnas),
            2-(1-1/self.nfilas)]
        surface.blit(
            label,
            (
                pos[0]*self.rect_label[0] + (self.espacio[0]/n_esp[0]*(pos[0]+1)),
                pos[1]*self.rect_label[1] + (self.espacio[1]/n_esp[1]*(pos[1]+1))
            )
        )

    # self => pygame.Surface
    def crear_imagen(self):
        imagen = pygame.Surface((self.rect_px[0], self.rect_px[1]))
        imagen.fill(self.color_fondo)
        self.draw_label(self.title_vidas_img, imagen, [0, 0])
        self.draw_label(self.time_img, imagen, [0, 1])
        self.draw_label(self.title_score_img, imagen, [1, 0])
        self.draw_label(self.fuel_img, imagen, [1, 1])
        #self.draw_label(self.title_score_total_img, imagen, [2, 0])
        #self.draw_label(self.score_total_img, imagen, [2, 1])
        return imagen

    # self => pygame.Surface
    def crear_fondo(self):
        surface_fondo = pygame.Surface((self.rect_px[0], self.rect_px[1]))
        surface_fondo.fill(self.color_fondo)
        return surface_fondo

    # self => pygame.Surface
    def crear_label(self, text, color, color_fondo):
        surface = pygame.Surface((
            self.rect_label[0],
            self.rect_label[1]))
        surface.fill(color_fondo)
        text = self.font.render(text, 1, color)
        surface.blit(text, [
            self.rect_label[0] / 2 - text.get_width() / 2,
            self.rect_label[1] / 2 - text.get_height() / 2])
        return surface

    # self => pygame.Surface
    def crear_title_vidas_img(self):
        text = "TIME"
        return self.crear_label(text, self.color_letra_titulos, self.color_fondo_label_1)

    # self => pygame.Surface
    def crear_time_img(self):
        text = str(self.fase.game.seg)
        return self.crear_label(text, self.color_letra_puntuaciones, self.color_fondo_label_2)

    # self => pygame.Surface
    def crear_title_score_img(self):
        text = "FUEL"
        return self.crear_label(text, self.color_letra_titulos, self.color_fondo_label_1)

    # self => pygame.Surface
    def crear_fuel_img(self):
        text = str(self.fase.fuel)
        return self.crear_label(text, self.color_letra_puntuaciones, self.color_fondo_label_2)

    # self => pygame.Surface
    def crear_title_score_total_img(self):
        text = "TOTAL"
        return self.crear_label(text, self.color_letra_titulos, self.color_fondo_label_1)

    # self => pygame.Surface
    def crear_score_total_img(self):
        text = str(self.fase.total_score)
        return self.crear_label(text, self.color_letra_puntuaciones, self.color_fondo_label_2)

    # self => None
    def eventos(self):
        new_image = False

        if self.game.seg > self.seg_new_image:
            self.time_img = self.crear_time_img()
            self.seg_new_image = self.game.seg
            new_image = True

        if self.game.dec != self.dec_new_image:
            if self.fase.fuel > 0:
                self.fase.fuel -= 1
                self.fuel_img = self.crear_fuel_img()
                self.dec_new_image = self.game.dec
                new_image = True
                if self.fase.fuel == 0:
                    #self.fase.game_over = True
                    pass

        if new_image:
            self.imagen = self.crear_imagen()


    # self => None
    def resize(self):
        self.rect_px = self.fase.ventana.game_px_2_window_px(self.rect)
        self.set_surfaces()
