# ==========================================
#
# Pygame Arkanoid
# Autor: manuel.mayo.lado@gmail.com
#
# ==========================================

import os
import pygame
import random

from app.Cohete import *
from app.Asteroide import *


class RectJuego:
    """
    Gestión del rectágulo jugable
    """
    def __init__(self, game, fase):
        """
        ::args
        :game: Clase Game
        :fase: Clase Fase
        :rect[list(int)]: Ancho y alto del rectángulo jugable
        """
        # colors
        self.color_marco = 205, 205, 200
        self.color_background = 20, 20, 20
        # Clase game parent
        self.game = game
        # Clase Fase parent
        self.fase = fase
        # Función para transformar las medidas (game_size a px)
        self.game_px_2_window_px = self.fase.ventana.game_px_2_window_px
        # medidas del rectángulo de juego
        self.rect = fase.rect_jugable
        # medidas del rectangulo en la ventana
        self.rect_px = self.game_px_2_window_px(self.rect)
        # ancho del marco
        self.marco = game.config.game_screen.side_frame_size
        # images
        self.images_dir = self.game.config.images.dir
        self.image_background = self.game.config.background.file
        # Cohete
        self.cohete = Cohete(
            self,
            [game.config.cohete.width,game.config.cohete.height],
            game.config.cohete.speed
            )
        # Asteroides
        self.asteroide_radio = self.game.config.asteroide.radio
        self.lista_asteroides = []
        self.generation = self.game.config.asteroide.generation
        self.seg_generation = 'init generation'
        # atributos que varian con el tamaño de la ventana
        self.set_surfaces()

    # self => None
    def set_surfaces(self):
        # pygame marco surface
        self.marco_img = self.crear_marco()
        # pygame fondo surface
        self.fondo_img = self.crear_fondo()
        # pygame imagen total
        self.imagen = self.crear_imagen()
        # game over image
        self.image_game_over = self.crear_game_over_img()
        # dibujar?
        self.actualizar_dibujo = 1

    # self => None
    def draw(self):
        # fondo
        self.draw_imagen()
        # elementos
        self.cohete.draw()
        self.draw_asteroides()
        # marco
        self.draw_marco()
        if self.fase.game_over:
            self.draw_game_over()

    # self => None
    def draw_imagen(self):
       self.fase.surface.blit(
            self.imagen,
            (0, self.fase.RectInfo.rect_px[1]))

    # self => None
    def draw_marco(self):
        self.fase.surface.blit(
            self.marco_img,
            (0, self.fase.RectInfo.rect_px[1]))

    # self => None
    def draw_asteroides(self):
        for asteroide in self.lista_asteroides:
            asteroide.draw()

    def draw_game_over(self):
        self.fase.surface.blit(
            self.image_game_over,
            (0, self.fase.RectInfo.rect_px[1]))

    # self => pygame.Surface
    def crear_fondo(self):
        surface_fondo = pygame.Surface(self.rect_px)
        if self.image_background:
            background_image_path = os.path.join(self.images_dir,self.image_background)
            if os.path.exists(background_image_path):
                background_surface = pygame.image.load(background_image_path)
                background_surface = pygame.transform.smoothscale(
                    background_surface,
                    self.rect_px,
                    )
                surface_fondo.blit(background_surface,(0,0))
        else:
            surface_fondo.fill(self.color_background)
        return surface_fondo

    # self => pygame.Surface
    def crear_marco(self):
        rect_marco_izq = pygame.Rect(
            0,
            0,
            self.game_px_2_window_px(self.marco),
            self.rect_px[1])
        rect_marco_der = pygame.Rect(
            self.rect_px[0] - self.game_px_2_window_px(self.marco),
            0,
            self.rect_px[0],
            self.rect_px[1])
        rect_marco_top = pygame.Rect(
            0,
            0,
            self.rect_px[0],
            self.game_px_2_window_px(self.marco))
        marco_img = pygame.Surface(self.rect_px, pygame.SRCALPHA, 32)
        pygame.draw.rect(marco_img, self.color_marco, rect_marco_izq)
        pygame.draw.rect(marco_img, self.color_marco, rect_marco_der)
        pygame.draw.rect(marco_img, self.color_marco, rect_marco_top)
        return marco_img

    # self => pygame.Surface
    def crear_imagen(self):
        imagen = pygame.Surface(self.rect_px)
        imagen.blit(self.fondo_img, (0,0))
        return imagen

    # self => pygame.Surface
    def crear_game_over_img(self):
        text = "GAME OVER"
        surface = pygame.Surface((self.rect[0]/2, self.rect[1]/10), pygame.SRCALPHA, 32)

        self.font = pygame.font.Font(None,10)
        text = self.font.render(text, 1, [0,0,200])
        surface.blit(text, [
            0,
            0])
        return surface

    # self => None
    def eventos(self):
        self.cohete.movimiento()

        for asteroide in self.lista_asteroides:
            asteroide.movimiento()
            if asteroide.pos.y > self.rect[1]+asteroide.radio*2:
                self.lista_asteroides.remove(asteroide)

        if ((self.game.seg == 0 or self.game.seg-self.seg_generation == self.generation) 
        and self.game.seg != self.seg_generation):
            self.seg_generation = self.game.seg
            self.new_asteroide()


    # self => None
    def new_asteroide(self):
        pos = Punto(
            random.randrange(0,self.rect[0]-self.asteroide_radio),
            -self.asteroide_radio
        )
        self.lista_asteroides.append(
            Asteroide(
                self,
                self.asteroide_radio,
                pos
            )
        )

    # self => None
    def resize(self):
        self.rect_px = self.game_px_2_window_px(self.rect)
        self.set_surfaces()
        self.cohete.resize()
        for asteroide in self.lista_asteroides:
            asteroide.resize()
