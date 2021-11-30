# main script
import pygame as pg

from classes import Graph, Edge, Vertex, V
from constants import *

from random import randint


def random_graph(n: int, e: int) -> Graph:
    g = Graph(set(), set())

    vertices = [V(randint(100, 700), randint(100, 500)) for _ in range(n)]
    g.add_vertex(*vertices)
    for _ in range(e):
        v1 = v2 = vertices[randint(0, n-1)]
        while v1 == v2:
            v2 = vertices[randint(0, n-1)]
        g.add_edge(v1, v2, 1)

    return g


pg.init()

screen = pg.display.set_mode(SCREEN_DIM)
done = False
clock = pg.time.Clock()

g = random_graph(10, 12)

while not done:
    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                done = True
    
    mouse_pos = pg.mouse.get_pos()
    selected = g.get_selected(mouse_pos)

    screen.fill(BG_COLOR)

    g.draw(screen, selected)

    pg.display.update()
    clock.tick(30)
