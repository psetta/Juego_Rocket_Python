# ==========================================
#
# Pygame Arkanoid
# Autor: manuel.mayo.lado@gmail.com
#
# ==========================================

import pygame
import os

from app.Punto import *
from pygame.locals import *


class Cohete:
    """
    Gestión de la pala del jugador
    """
    def __init__(self, rect_juego, rect, velocidad):
        """
        ::args
        :rect_juego: Clase RectJuego
        :rect[list(int)]: Ancho y alto de la cohete
        :velocidad[int]: Velocidad a la que se mueve la cohete
        """
        # Clase RectJuego parent
        self.rect_juego = rect_juego
        # Función para transformar las medidas (game_size a px)
        self.game_px_2_window_px = self.rect_juego.game_px_2_window_px
        # tamaño del rectangulo de colisón del cohete
        self.rect = rect
        self.ancho, self.alto = self.rect
        self.rect_px = [
            self.game_px_2_window_px(self.ancho),
            self.game_px_2_window_px(self.alto)
        ]
        # image
        self.images_dir = self.rect_juego.game.config.images.dir
        self.image_name = self.rect_juego.game.config.cohete.image
        self.image_path = os.path.join(self.images_dir,self.image_name)
        self.image_rect = [
            self.rect_juego.game.config.cohete.image_width,
            self.rect_juego.game.config.cohete.image_height
        ]
        self.ancho_image, self.alto_image = self.image_rect
        self.plus_image_pos_y = self.rect_juego.game.config.cohete.image_plus_height
        # relación entre el rect de la cohete y de RectJuego
        self.relacion_rects = self.rect[0]/self.rect_juego.rect[0]
        # relación entre el alto y el ancho de la cohete
        self.relacion_aa = self.rect[1]/self.rect[0]
        # velocidad de la cohete
        self.velocidad = velocidad
        # posición (empieza en el centro y abajo)
        self.pos = Punto(
            rect_juego.rect[0]/2-rect[0]/2,
            rect_juego.rect[1]-(rect[1]+rect_juego.rect_px[1]/300)
        )
        # atributos que varian con el tamaño de la ventana
        self.set_surfaces()

    # self => None
    def set_surfaces(self):
        self.rect_px = [
            self.game_px_2_window_px(self.ancho),
            self.game_px_2_window_px(self.alto)
        ]
        self.image_rect_px = [
            self.game_px_2_window_px(self.ancho_image),
            self.game_px_2_window_px(self.alto_image)
        ]
        self.plus_image_pos_y_px = self.game_px_2_window_px(self.plus_image_pos_y)
        # rectangulo Pygame de la cohete
        self.rect_pygame = pygame.Rect((0,0),self.rect_px)
        # imagen Pygame de la cohete
        self.cohete_image = pygame.image.load(self.image_path)
        self.rect_cohete = [
            int(self.image_rect_px[0]),
            int(self.image_rect_px[1])
        ]
        self.cohete_image = pygame.transform.smoothscale(self.cohete_image,self.rect_cohete)
        self.cohete_surf = self.crear_cohete_surf()

    # self => Punto
    def pos_in_surface(self):
        return Punto(
            self.pos.x,
            self.pos.y+self.rect_juego.fase.RectInfo.rect[1])

    # self => float
    def pos_centro(self):
        return self.pos.x+self.ancho/2

    # self => int
    def movimiento(self):
        key_pressed = pygame.key.get_pressed()
        velocidad_px = self.game_px_2_window_px(self.velocidad)
        if key_pressed[K_LEFT] or key_pressed[K_a]:
            pos_fut = Punto(self.pos.x-self.velocidad,self.pos.y)
            if self.colision_izq(pos_fut):
                self.pos.x = self.rect_juego.marco
                return -1
            self.pos.x -= self.velocidad
        if key_pressed[K_RIGHT] or key_pressed[K_d]:
            pos_fut = Punto(self.pos.x+self.velocidad,self.pos.y)
            if self.colision_der(pos_fut):
                self.pos.x = (self.rect_juego.rect[0]-(self.ancho+self.rect_juego.marco))
                return 1
            self.pos.x += self.velocidad

    # self => None
    def draw(self):
        rect_px_window = self.game_px_2_window_px(self.pos_in_surface())
        # dibujar rectangulo colisión
        """
        self.rect_juego.fase.surface.blit(
            self.cohete_surf,
            rect_px_window
        )
        """
        # dibujar cohete
        rect_px = [
            rect_px_window[0]+(self.rect_px[0]-self.rect_cohete[0])/2,
            (rect_px_window[1]+(self.rect_px[1]-self.rect_cohete[1])/2)+self.plus_image_pos_y_px
        ]
        self.rect_juego.fase.surface.blit(
            self.cohete_image,
            rect_px
        )

    # self => pygame.Surface
    def crear_cohete_surf(self):
        cohete_surf = pygame.Surface(
            (self.game_px_2_window_px(self.ancho), self.game_px_2_window_px(self.alto)),
            pygame.SRCALPHA,
            32
        )
        rect = pygame.Rect(0,0,self.rect_px[0],self.rect_px[1])
        pygame.draw.rect(cohete_surf, [150,150,150], rect)
        #cohete_surf.blit(self.cohete_image, (0,0))
        return cohete_surf

    # self, Punto => Boolean
    def colision_izq(self, pos):
        return pos.x <= self.rect_juego.marco

    # self, Punto => Boolean
    def colision_der(self, pos):
        return (pos.x+self.ancho >=
            self.rect_juego.rect[0]-self.rect_juego.marco)

    # self => None
    def resize(self):
        self.set_surfaces()