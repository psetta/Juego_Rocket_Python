import pygame.gfxdraw
import sys
import os
import ctypes
import json

from app.Config import config
from app.Ventana import *
from app.Fase import *


class Game:
    # self => None
    def __init__(self):
        """
        Clase principal del juego
        """
        # configuración
        self.config = config  

        # title name
        self.title_name = config.info.name

        # Ejecuciones de bucle y frames por segundo
        self.max_bps = config.loops.max_bps
        self.bps = config.loops.bps
        self.fps = config.loops.fps
        self.seg = 0
        self.dec = 0

        self.list_bps = [x%(int(self.max_bps/self.bps))==0 for x in range(self.max_bps)]
        self.list_fps = [x%(int(self.max_bps/self.fps))==0 for x in range(self.max_bps)]

        # desscaling DPI
        if os.name == 'nt' and sys.getwindowsversion()[0] >= 6:
            ctypes.windll.user32.SetProcessDPIAware()

        # pygame init
        pygame.init()

        # window title name
        pygame.display.set_caption(self.title_name)

        # Clase Ventana
        self.ventana = Ventana(self)

        # Clase Fase
        self.fase = Fase(
            self,
            self.ventana,
            self.ventana.fase_rect)

    # self => None
    def start(self):
        """
        Iniciar el juego
        """
        # Juego en ejecución
        self.run = True
        # iteración actual
        iteration = 0

        # bucle principal del Juego
        while self.run:

            reloj = pygame.time.Clock()

            # Dibujado
            if self.list_fps[iteration]:
                self.draw()

            # FASE eventos
            if self.list_bps[iteration]:
                self.fase.eventos()

            # MAIN eventos
            self.eventos()

            # FPS
            reloj.tick(self.max_bps)

            # iteraciones
            iteration += 1

            dec_range = list(range(0,self.max_bps,int(self.max_bps/10)))
            if iteration in dec_range:
                self.dec += 1
                
            if iteration == self.max_bps:
                iteration = 0
                self.seg += 1
                self.dec = 0

    # self => None
    def draw(self):
        """
        Dibujar en la ventana todos los elementos del juego
        """
        self.fase.draw()
        self.ventana.draw()

    # self => None
    def eventos(self):
        """
        Gestión de los eventos del juego
        """
        for event in pygame.event.get():
            # EXIT
            if event.type == pygame.QUIT:
                self.quit()
                self.run = False
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                    self.quit()
                    self.run = False
            # RESIZE
            if event.type == pygame.VIDEORESIZE:
                self.ventana.resize(event.w, event.h)
                self.fase.resize()

    #  => None
    @staticmethod
    def quit():
        """
        Cerrar el juego
        """
        pygame.display.quit()


# main
if __name__ == "__main__":
    game = Game()
    game.start()
