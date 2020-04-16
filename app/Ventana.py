# ==========================================
#
# Pygame Arkanoid
# Autor: manuel.mayo.lado@gmail.com
#
# ==========================================

from typing import List, Any, Union

import pygame

from app.Punto import *


class Ventana:
    """
    Gestión de la ventana usando el módulo Pygame
    """
    def __init__(self, game):
        """
        @args
            game: Game Class
        """
        # Clase Game parent
        self.game = game

        # Color de fondo
        self.color_fondo = 205, 205, 200

        # Game internal sizes
        self.rect = [game.config.game_screen.width,
                    game.config.game_screen.height]

        # Relación entre el ancho y el alto del rectángulo
        self.rel_rect = self.rect[0]/self.rect[1]

        # Relación entre las medidas de la ventana y el monitor
        self.window_monitor_relation = game.config.window.monitor_relation

        # Medidas del rectángulo de juego
        self.rel_game_rect = min(1, game.config.window.content_relation)
        self.fase_rect = [self.rect[0]*self.rel_game_rect, self.rect[1]*self.rel_game_rect]

        # relacion w/h del rectángulo de juego
        self.rel_fase_rect = self.fase_rect[0]/self.fase_rect[1]

        # relación (rect_game - rect_fase)
        self.rel_r_rg = self.rect[0]/self.fase_rect[0], self.rect[1]/self.fase_rect[1]

        # Información del monitor
        self.info_object = pygame.display.Info()
        self.monitor_rect = [self.info_object.current_w, self.info_object.current_h]

        # Medidas (px) iniciales de la ventana
        if self.monitor_rect[0] < self.monitor_rect[1]:
            ventana_rect_x = self.monitor_rect[0]*self.window_monitor_relation
            self.ventana_rect = [round(ventana_rect_x), round(ventana_rect_x/self.rel_rect)]
        else:
            ventana_rect_y = self.monitor_rect[1]*self.window_monitor_relation
            self.ventana_rect = [round(ventana_rect_y*self.rel_rect),round(ventana_rect_y)]

        # Medidas mínimas de la ventana (px)
        self.ventana_rect_min = self.ventana_rect.copy()

        # Medidas (px) del rectangulo de juego
        self.rect_px = self.ventana_rect.copy()

        # Relación entre las medidas internas del juego y las medidas de la ventana (px)
        self.rel_px = self.rect_px[0] / self.rect[0]

        # Espacio lateral y superior
        self.set_espacio()

        # display update all window (?)
        self.display_update_all = 0

        # crear surfaces
        self.set_surfaces()

        None

    # self => None
    def set_surfaces(self):
        # pygame display
        if self.game.config.window.fullscreen:
            flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        else:
            flags = pygame.RESIZABLE
        self.pygame = pygame.display.set_mode(
                    self.ventana_rect,
                    flags
                    )
        # pygame Rect Game
        self.rect_game_pygame = pygame.Rect(
            self.espacio,
            self.game_px_2_window_px(self.rect))
        # pygame superficie
        self.pygame_game_surface = self.crear_game_surface()

    # self => None
    def set_espacio(self):
        self.espacio = [
            (self.ventana_rect[0]-self.game_px_2_window_px(self.fase_rect[0]))/2,
            (self.ventana_rect[1]-self.game_px_2_window_px(self.fase_rect[1]))/2
            ]

    # self => None
    def draw(self):
        self.dibujar_fondo_total()
        self.dibujar_surface_game()
        if self.display_update_all:
            pygame.display.update()
            self.display_update_all = 0
        else:
            pygame.display.update(self.rect_game_pygame)

    # self => None
    def dibujar_fondo_total(self):
        self.pygame.fill(self.color_fondo)

    # self => None
    def dibujar_surface_game(self):
        self.pygame.blit(
            self.pygame_game_surface,
            self.espacio
            )

    # self => None
    def crear_game_surface(self):
        surface = pygame.Surface(self.game_px_2_window_px(self.rect))
        return surface

    # self, numeric/sequence => numeric
    def game_px_2_window_px(self, n):
        if type(n) == int or type(n) == float or type(n) == Punto:
            return round(n * self.rel_px)
        else:
            return [round(i*self.rel_px) for i in n]

    def resize(self, w, h):
        new_w = max(w, self.ventana_rect_min[0])
        new_h = max(h, self.ventana_rect_min[1])
        # medidas del juego
        game_h = min(new_h / self.rel_r_rg[1], new_h)
        game_w = game_h * self.rel_rect
        if game_w > new_w:
            game_w = min(new_w / self.rel_r_rg[0], new_w)
            game_h = game_w / self.rel_rect
        # medidas (px) totales de la ventana
        self.ventana_rect = [new_w, new_h]
        # medidas (px) del rectángulo de juego
        self.rect_px = [game_w, game_h]
        # relación px game/ventana
        self.rel_px = self.rect_px[0] / self.rect[0]
        # espacio
        self.set_espacio()
        # declaracion de variables
        self.set_surfaces()
        # actualizar toda la ventana
        self.display_update_all = 1
        # display update
        pygame.display.update()
