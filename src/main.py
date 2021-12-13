# main script
from constants import *
import pygame as pg
from engine import Editor, AlgorithmRunner
from classes import random_graph


if __name__ == "__main__":
    # initialize pygame and pygame.font
    pg.init()
    pg.font.init()

    # set up screen and font
    screen = pg.display.set_mode(SCREEN_DIM)
    font = pg.font.SysFont('Consolas', FONT_SIZE, False)

    # starting_graph = random_graph(8, 20)

    # use the editor to create a connected graph
    graph = Editor(screen, font).run()
    while True:
        AlgorithmRunner(screen, font, graph).run()
        graph = Editor(screen, font, graph).run()
