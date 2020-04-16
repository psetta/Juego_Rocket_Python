# ==========================================
#
# Pygame Arkanoid
# Autor: manuel.mayo.lado@gmail.com
#
# ==========================================

from app.RectJuego import *
from app.RectInfo import *


class Fase:
    """
    Gestión del rectágulo del juego. Se divide en 2 rectángulos:
        > Rect de información: Donde se muestra la información
          del juego (Vidas, Score, Score Máximo)
        > Rect jugable: Donde el jugador puede interaccionar
    """
    def __init__(self, game, ventana, rect):
        """
        @args
            game: Clase Game.
            ventana: Clase Ventana.
            rect: [list(int)]. Ancho y alto del rectángulo de juego
        """
        # Clase Game parent
        self.game = game
        # Clase Ventana parent
        self.ventana = ventana
        # ancho y alto de la fase de juego
        self.rect = rect
        # relación entre el rectángulo jugable y de información
        self.relac = game.config.game_screen.percent_height
        # rect jugable
        self.rect_jugable = [self.rect[0], round(self.rect[1] * self.relac)]
        # rect info
        self.rect_info = [self.rect[0], self.rect[1] - self.rect_jugable[1]]
        # info
        self.vidas = game.config.score.init_lives
        self.score = 0
        self.total_score = 0
        self.fuel = 100
        self.game_over = False
        self.game_over_screen = False
        # RectJuego
        self.RectJuego = RectJuego(self.game, self)
        # RectInfo
        self.RectInfo = RectInfo(self.game, self)
        # crear surface
        self.set_surfaces()

    # self => None
    def set_surfaces(self):
        # pygame superficie
        self.surface = self.crear_surface()

    # self => pygame.Surface
    def crear_surface(self):
        surface = pygame.Surface(self.ventana.game_px_2_window_px(self.rect))
        return surface

    # self, Ventana => None
    def draw(self):
        if self.game_over_screen:
            None
        elif self.game_over:
            self.RectInfo.draw()
            self.ventana.pygame_game_surface.blit(self.surface, (0, 0))
            self.game_over_screen = True
        else:
            self.RectJuego.draw()
            self.RectInfo.draw()
            self.ventana.pygame_game_surface.blit(self.surface, (0, 0))

    def eventos(self):
        self.RectJuego.eventos()
        self.RectInfo.eventos()

    # self, Ventana => None
    def resize(self):
        self.set_surfaces()
        self.RectJuego.resize()
        self.RectInfo.resize()
