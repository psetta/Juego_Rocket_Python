# ==========================================
#
# Pygame Arkanoid
# Autor: manuel.mayo.lado@gmail.com
#
# ==========================================

import pygame
import math
import os

from app.Punto import *
from pygame.locals import *


class Asteroide:
    """
    Gestión de la asteroide
    """
    def __init__(self, rect_juego, radio, pos):
        """
        ::args
        :rect_juego: Clase RectJuego
        :radio[int]: Radio del asteroide
        :pos[Punto]: Posición del asteroide
        """
        # RectJuego
        self.rect_juego = rect_juego
        # Función para transformar las medidas (game_size a px)
        self.game_px_2_window_px = self.rect_juego.game_px_2_window_px
        # tamaño del radio
        self.radio = radio
        # relación entre la ventana y el radio de la asteroide
        self.relacion_radio =  self.radio / self.rect_juego.rect[0]
        # posición
        self.pos = pos
        # velocidad
        self.speed = self.rect_juego.game.config.asteroide.speed
        # color
        self.color = 200, 100, 100
        # image
        self.images_dir = self.rect_juego.game.config.images.dir
        self.image_name = self.rect_juego.game.config.asteroide.image
        self.image_path = os.path.join(self.images_dir,self.image_name)
        self.image_rect = [
            self.rect_juego.game.config.asteroide.image_width,
            self.rect_juego.game.config.asteroide.image_height
        ]
        self.ancho_image, self.alto_image = self.image_rect
        self.set_surfaces()

    # self => None
    def set_surfaces(self):
        self.rect_px = [
            self.game_px_2_window_px(self.radio),
            self.game_px_2_window_px(self.radio)
        ]
        self.image_rect_px = [
            self.game_px_2_window_px(self.ancho_image),
            self.game_px_2_window_px(self.alto_image)
        ]
        # rectangulo Pygame del asteroide
        self.rect_pygame = pygame.Rect((0,0),self.rect_px)
        # imagen Pygame del asteroide
        self.asteroide_image = pygame.image.load(self.image_path)
        self.rect_asteroide = [
            int(self.image_rect_px[0]),
            int(self.image_rect_px[1])
        ]
        self.asteroide_image = pygame.transform.smoothscale(self.asteroide_image,self.rect_asteroide)
        self.asteroide_surf = self.crear_asteroide_surf()

    # self => Punto
    def pos_in_surface(self,pos):
        return Punto(
            pos.x,
            pos.y+self.rect_juego.fase.RectInfo.rect[1])

    def movimiento(self):
        self.pos += Punto(0,self.speed)

    # self => None
    def draw(self):
        self.draw_asteroide()

    #self => None
    def draw_asteroide(self):
        pos_i = self.pos_in_surface(self.pos)
        pos_px = self.game_px_2_window_px(pos_i)
        """
        pygame.gfxdraw.filled_circle(self.rect_juego.fase.surface,
                                self.game_px_2_window_px(pos_i.x),
                                self.game_px_2_window_px(pos_i.y),
                                self.game_px_2_window_px(self.radio),
                                self.color)
        pygame.gfxdraw.aacircle(self.rect_juego.fase.surface,
                                self.game_px_2_window_px(pos_i.x),
                                self.game_px_2_window_px(pos_i.y),
                                self.game_px_2_window_px(self.radio),
                                self.color)
        """
        # dibujar asteroide
        rect_px_window = self.game_px_2_window_px(self.pos)
        rect_px = [
            rect_px_window[0]+(self.rect_px[0]-self.rect_asteroide[0])/2,
            rect_px_window[1]+(self.rect_px[1]-self.rect_asteroide[1])/2
        ]
        self.rect_juego.fase.surface.blit(
            self.asteroide_image,
            rect_px
        )

    # self => pygame.Surface
    def crear_asteroide_surf(self):
        asteroide_surf = pygame.Surface(
            (self.game_px_2_window_px(self.radio), self.game_px_2_window_px(self.radio)),
            pygame.SRCALPHA,
            32
        )
        rect = pygame.Rect(0,0,self.rect_px[0],self.rect_px[1])
        pygame.draw.rect(asteroide_surf, [150,150,150], rect)
        #asteroide_surf.blit(self.asteroide_image, (0,0))
        return asteroide_surf

    def resize(self):
        self.set_surfaces()
