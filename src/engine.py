# application engine
from typing import Optional
import pygame as pg
from pygame.constants import MOUSEWHEEL

from classes import Graph, Edge, Vertex, V
from constants import *


class Editor:
    def __init__(self, screen: pg.Surface, font: pg.font.Font, graph=Graph(set(), set())) -> None:
        self.screen = screen
        self.font = font

        self._clock = pg.time.Clock()
        self._done = False
        self.graph = graph
        self._selected: Optional[Vertex | Edge] = None
        self._state = "editor.free"

        self._from_vertex: Optional[Vertex] = None
        self._new_weight = 0

        self._state_map = {
            "editor.free": self.state_editor_free,
            "editor.clicking": self.state_editor_clicking,
            "editor.dragging": self.state_editor_dragging,
            "editor.holding_edge": self.state_editor_holding_edge,
        }

    def state_editor_free(self, mouse_pos: tuple[int, int]) -> None:
        """
        editor.free state input handler
        
        This is the default, resting state of the editor.
        """
        self._selected = self.graph.get_selected(mouse_pos)
        self._from_vertex = None
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self._done = True
                
                case pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # left click on empty space creates a vertex
                        if not self._selected:
                            self.graph.add_vertex(V(*mouse_pos))
                        # left click on vertex will either move (drag) 
                        # or create an edge (release w/o moving)
                        elif isinstance(self._selected, Vertex):
                            self._state = "editor.clicking"
                    
                    elif event.button == 3:
                        # right clicking on a vertex or edge removes it
                        match self._selected:
                            case Vertex():
                                self.graph.remove_vertex(self._selected)
                            case Edge():
                                self.graph.remove_edge(self._selected)
                
                case pg.MOUSEWHEEL:
                    # scrolling modifies edge weight
                    if isinstance(self._selected, Edge):
                        self.graph.modify_edge_weight(self._selected, max(0, self._selected.weight + event.y))
    
    def state_editor_clicking(self, mouse_pos: tuple[int, int]) -> None:
        """
        editor.clicking state input handler
        
        In this state, a vertex has been clicked, and the application must
        determine if the user intends to move the vertex or to create a 
        new edge from that vertex.
        """
        self._selected = self.graph.get_selected(mouse_pos)
        self._from_vertex = None
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self._done = True
                
                case pg.MOUSEMOTION:
                    self._state = "editor.dragging"

                case pg.MOUSEBUTTONUP:
                    # releasing left click without moving the mouse will
                    # create a new edge from the selected vertex
                    if event.button == 1:
                        if isinstance(self._selected, Vertex):
                            self._from_vertex = self._selected
                            self._state = "editor.holding_edge"
    
    def state_editor_dragging(self, mouse_pos: tuple[int, int]) -> None:
        """
        editor.dragging state input handler
        
        In this state, the selected vertex follows the mouse position 
        until left click is released.
        """
        self._from_vertex = None
        # check if we missed a mouse release
        if not pg.mouse.get_pressed()[0]:
            self._state = "editor.free"
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self._done = True
                
                case pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        self._state = "editor.free"
        
        if isinstance(self._selected, Vertex):
            self.graph.move_vertex(self._selected, mouse_pos)

    def state_editor_holding_edge(self, mouse_pos: tuple[int, int]) -> None:
        """
        editor.holding_edge state input handler
        
        In this state, the user has clicked a vertex and there is a 
        temporary edge drawn between the clicked vertex and the mouse.
        If another vertex is clicked, a real edge is created between
        the two.
        """
        self._selected = self.graph.get_selected(mouse_pos)
        # can only select vertices while placing an edge
        if not isinstance(self._selected, Vertex):
            self._selected = None
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self._done = True
                
                case pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # if clicking on another vertex, create new edge
                        if self._selected and self._selected != self._from_vertex:
                            self.graph.add_edge(self._from_vertex, self._selected, self._new_weight)
                            self._from_vertex = None
                            self._new_weight = 0
                            self._state = "editor.free"

                    elif event.button == 3:
                        # cancel new edge
                        self._from_vertex = None
                        self._new_weight = 0
                        self._state = "editor.free"
                
                case pg.MOUSEWHEEL:
                    # scrolling changes weight of new edge
                    self._new_weight = max(0, self._new_weight + event.y)
        
    def draw_temp_edge(self, mouse_pos: tuple[int, int]) -> None:
        """Draws the temporary edge from selected vertex to mouse position."""
        a, b = self._from_vertex, mouse_pos

        w_text = self.font.render(str(self._new_weight), True, EDGE_HOVER_COLOR, BG_COLOR)
        w_text_border_size = max(w_text.get_width(), w_text.get_height())
        midpoint = ((a.pos[0] + b[0]) // 2, (a.pos[1] + b[1]) // 2)

        # attempt to normalize line thickness
        diff = (abs(a.pos[0] - b[0]), abs(a.pos[1] - b[1]))
        t = int(min(diff) / max(diff) + (EDGE_HOVER_WIDTH / 1.5)) if all(diff) else 0
        pg.draw.line(self.screen, EDGE_HOVER_COLOR, a.pos, b, width=EDGE_HOVER_WIDTH+t)

        # draw edge weight at center point
        self.screen.fill(
            EDGE_HOVER_COLOR,
            (
                midpoint[0] - (w_text_border_size + 2 * EDGE_HOVER_WIDTH) // 2,
                midpoint[1] - (w_text_border_size + 2 * EDGE_HOVER_WIDTH) // 2,
                w_text_border_size + 2 * EDGE_HOVER_WIDTH,
                w_text_border_size + 2 * EDGE_HOVER_WIDTH,
            ),
        )
        self.screen.fill(
            BG_COLOR,
            (
                midpoint[0] - (w_text_border_size + 2) // 2,
                midpoint[1] - (w_text_border_size + 2) // 2,
                w_text_border_size + 2,
                w_text_border_size + 2,
            ),
        )
        self.screen.blit(
            w_text,
            (
                midpoint[0] - w_text.get_width() // 2,
                midpoint[1] - w_text.get_height() // 2,
            ),
        )

    def run(self) -> Graph:
        """Start and run the editor. Returns the created graph."""
        pg.display.set_caption(f"Kruskal's Algorithm - Create a Connected Graph")

        while not self._done:
            mouse_pos = pg.mouse.get_pos()
            
            # process input based on current state
            self._state_map[self._state](mouse_pos)

            self.screen.fill(BG_COLOR)
            self.graph.draw(self.screen, self._selected, self.font)

            # draw edge-in-progress if needed
            if self._from_vertex:
                self.draw_temp_edge(mouse_pos)
                self._from_vertex.draw(self.screen, VERTEX_HOVER_COLOR, VERTEX_HOVER_RADIUS)
            
            match self.graph.usable:
                case (False, msg):
                    m_color = ERROR_COLOR
                case (True, msg):
                    m_color = SUCCESS_COLOR
            
            m_text = self.font.render(msg, True, m_color)
            self.screen.blit(m_text, (10, SCREEN_DIM[1] - m_text.get_height() - 10))

            pg.display.update()
            self._clock.tick(FPS)
        
        return self.graph
