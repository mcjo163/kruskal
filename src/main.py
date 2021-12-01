# main script
from constants import *
import pygame as pg
from engine import Editor, AlgorithmRunner


if __name__ == "__main__":
    # initialize pygame and pygame.font
    pg.init()
    pg.font.init()

    # set up screen and font
    screen = pg.display.set_mode(SCREEN_DIM)
    font = pg.font.SysFont('Consolas', FONT_SIZE, False)

    # use the editor to create a connected graph
    graph = Editor(screen, font).run()
    AlgorithmRunner(screen, font, graph).run()
