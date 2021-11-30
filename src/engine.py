# application engine
from typing import Optional
import pygame as pg

from classes import Graph, Edge, Vertex, V
from constants import *


# application states
#
# editor.free:          default state
# editor.clicking:      vertex has been clicked, but not moved
# editor.dragging:      currently dragging a vertex
# editor.holding_edge:  placing an edge

class Engine:
    def __init__(self) -> None:
        self.screen = pg.display.set_mode(SCREEN_DIM)
        self.clock = pg.time.Clock()
        self.done = False

        self._graph = Graph(set(), set())
        self._selected: Optional[Vertex | Edge] = None
        self._state = "editor.free"

        self._from_vertex: Optional[Vertex] = None

        self._state_map = {
            "editor.free": self.state_editor_free,
            "editor.clicking": self.state_editor_clicking,
            "editor.dragging": self.state_editor_dragging,
            "editor.holding_edge": self.state_editor_holding_edge,
        }

    def state_editor_free(self, mouse_pos: tuple[int, int]) -> None:
        self._selected = self._graph.get_selected(mouse_pos)
        self._from_vertex = None
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self.done = True
                
                case pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # left click on empty space creates a vertex
                        if not self._selected:
                            self._graph.add_vertex(V(*mouse_pos))
                        # left click on vertex will either move (drag) 
                        # or create an edge (release w/o moving)
                        elif isinstance(self._selected, Vertex):
                            self._state = "editor.clicking"
                    
                    elif event.button == 3:
                        # right clicking on a vertex or edge removes it
                        match self._selected:
                            case Vertex():
                                self._graph.remove_vertex(self._selected)
                            case Edge():
                                self._graph.remove_edge(self._selected)
    
    def state_editor_clicking(self, mouse_pos: tuple[int, int]) -> None:
        self._selected = self._graph.get_selected(mouse_pos)
        self._from_vertex = None
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self.done = True
                
                case pg.MOUSEMOTION:
                    self._state = "editor.dragging"

                case pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        if isinstance(self._selected, Vertex):
                            self._from_vertex = self._selected
                            self._state = "editor.holding_edge"
    
    def state_editor_dragging(self, mouse_pos: tuple[int, int]) -> None:
        self._from_vertex = None
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self.done = True
                
                case pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        self._state = "editor.free"
        
        if isinstance(self._selected, Vertex):
            self._graph.move_vertex(self._selected, mouse_pos)

    def state_editor_holding_edge(self, mouse_pos: tuple[int, int]) -> None:
        self._selected = self._graph.get_selected(mouse_pos)
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self.done = True
                
                case pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # if clicking on another vertex, create new edge
                        if isinstance(self._selected, Vertex) and self._selected != self._from_vertex:
                            self._graph.add_edge(self._from_vertex, self._selected, 1)
                            self._from_vertex = None
                            self._state = "editor.free"

                    elif event.button == 3:
                        # cancel new edge
                        self._from_vertex = None
                        self._state = "editor.free"
    
    def run(self) -> None:
        """Start and run the application."""
        pg.display.set_caption(f"Kruskal's Algorithm - Create a Connected Graph")
        pg.init()

        while not self.done:
            mouse_pos = pg.mouse.get_pos()
            
            self._state_map[self._state](mouse_pos)

            self.screen.fill(BG_COLOR)

            # draw edge-in-progress
            if self._from_vertex:
                a, b = self._from_vertex, mouse_pos
                # attempt to normalize line thickness
                diff = (abs(a.pos[0] - b[0]), abs(a.pos[1] - b[1]))
                t = int(min(diff) / max(diff) + (EDGE_HOVER_WIDTH / 1.5)) if all(diff) else 0
                pg.draw.line(self.screen, EDGE_HOVER_COLOR, a.pos, b, width=EDGE_HOVER_WIDTH+t)

            self._graph.draw(self.screen, self._selected)

            pg.display.update()
            self.clock.tick(FPS)
