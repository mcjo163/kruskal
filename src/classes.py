# classes for graph modeling
import pygame as pg
from typing import Optional
from math import sqrt

from constants import *


def pt_distance(a: tuple[int, int], b: tuple[int, int]) -> float:
    """Returns the Euclidean distance between two points."""
    x1, y1 = a
    x2, y2 = b
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def lies_between(
    point: tuple[int, int], a: tuple[int, int], b: tuple[int, int]
) -> bool:
    """Determines whether `point` lies between points `a` and `b`."""
    _a = pt_distance(a, b)
    _b = pt_distance(b, point)
    _c = pt_distance(point, a)
    return (_a ** 2 + _b ** 2 >= _c ** 2) and (_a ** 2 + _c ** 2 >= _b ** 2)


class Vertex:
    """Represents a vertex with positional information."""

    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos = pos
        self._edges: set[Edge] = set()

    def __str__(self) -> str:
        return f"V{self.pos}"

    def distance_to(self, point: tuple[int, int]) -> float:
        """Returns the distance from this vertex to a given point."""
        return pt_distance(self.pos, point)

    @property
    def deg(self) -> int:
        """The number of edges connected to this vertex."""
        return len(self._edges)

    def draw(self, surf: pg.Surface, color: tuple[int, int, int], radius: int) -> None:
        """Draws the vertex to the given `Surface`."""
        pg.draw.circle(surf, color, self.pos, radius)


class Edge:
    """Represents a weighted edge."""

    def __init__(self, a: Vertex, b: Vertex, weight: int) -> None:
        self.vertices = (a, b)
        self.weight = weight

        # add self to vertices' edge sets
        self.vertices[0]._edges.add(self)
        self.vertices[1]._edges.add(self)
    
    def __str__(self) -> str:
        return f"E({str(self.vertices[0])}->{str(self.vertices[1])})"

    def distance_to(self, point: tuple[int, int]) -> float:
        """Returns the perpendicular distance from this vertex to a given point."""
        x0, y0 = point
        x1, y1 = self.vertices[0].pos
        x2, y2 = self.vertices[1].pos

        # use formula if perpendicular distance makes sense
        if lies_between(point, (x1, y1), (x2, y2)):
            return abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)) / pt_distance(
                (x1, y1), (x2, y2)
            )

        # otherwise return distance to closest endpoint
        return min(pt_distance(point, (x1, y1)), pt_distance(point, (x2, y2)))

    def walk(self, start: Vertex) -> Vertex:
        """Walks this edge starting from `start`."""
        if start not in self.vertices:
            raise ValueError("Cannot walk from non-connected vertex.")
        return self.vertices[0 if start == self.vertices[1] else 1]

    def draw(
        self,
        surf: pg.Surface,
        font: pg.font.Font,
        color: tuple[int, int, int],
        width: int,
    ) -> None:
        """Draws the edge to the given `Surface`."""
        a, b = self.vertices

        w_text = font.render(str(self.weight), True, color, BG_COLOR)
        w_text_border_size = max(w_text.get_width(), w_text.get_height())
        midpoint = ((a.pos[0] + b.pos[0]) // 2, (a.pos[1] + b.pos[1]) // 2)

        # attempt to normalize line thickness
        diff = (abs(a.pos[0] - b.pos[0]), abs(a.pos[1] - b.pos[1]))
        t = int(min(diff) / max(diff) + (width / 1.5))

        # draw edge line
        pg.draw.line(surf, color, a.pos, b.pos, width=width + t)

        # draw edge weight at center point
        surf.fill(
            color,
            (
                midpoint[0] - (w_text_border_size + 2 * width) // 2,
                midpoint[1] - (w_text_border_size + 2 * width) // 2,
                w_text_border_size + 2 * width,
                w_text_border_size + 2 * width,
            ),
        )
        surf.fill(
            BG_COLOR,
            (
                midpoint[0] - (w_text_border_size + 2) // 2,
                midpoint[1] - (w_text_border_size + 2) // 2,
                w_text_border_size + 2,
                w_text_border_size + 2,
            ),
        )
        surf.blit(
            w_text,
            (
                midpoint[0] - w_text.get_width() // 2,
                midpoint[1] - w_text.get_height() // 2,
            ),
        )


class Graph:
    """Represents an edge-weighted graph."""

    def __init__(self, vertices: set[Vertex], edges: set[Edge]) -> None:
        self.vertices = vertices
        self.edges = edges

    def get_sorted_edges(self) -> list[Edge]:
        """Returns a list of the edges of the graph, sorted by weight."""
        return sorted(self.edges, key=lambda e: e.weight)

    def add_vertex(self, *vertices: Vertex) -> None:
        """Adds a vertex (or vertices) to the graph."""
        for v in vertices:
            self.vertices.add(v)

    def move_vertex(self, v: Vertex, pos: tuple[int, int]) -> None:
        """Moves a vertex to a new position."""
        if v not in self.vertices:
            raise ValueError("Cannot move nonexistent vertex.")
        v.pos = pos

    def remove_vertex(self, v: Vertex) -> None:
        """Removes a vertex from the graph."""
        if v not in self.vertices:
            raise ValueError("Cannot remove nonexistent vertex.")

        for edge in [e for e in self.edges if v in e.vertices]:
            self.remove_edge(edge)

        self.vertices.remove(v)

    def add_edge(self, a: Vertex, b: Vertex, weight: int) -> None:
        """Adds an edge between two vertices in the graph."""
        if a not in self.vertices or b not in self.vertices:
            raise ValueError("Cannot create edge with nonexistent vertex.")

        # ensure graph simplicity
        if a == b:
            return
        for e in self.edges:
            if set((a, b)) == set(e.vertices):
                # update edge weight to new desired value
                self.modify_edge_weight(e, weight)
                return

        self.edges.add(Edge(a, b, weight))

    def modify_edge_weight(self, e: Edge, weight: int) -> None:
        """Modifies the weight of an edge in the graph."""
        if e not in self.edges:
            raise ValueError("Cannot modify weight of nonexistent edge.")
        e.weight = weight

    def remove_edge(self, e: Edge) -> None:
        """Removes an edge between two vertices in the graph."""
        if e not in self.edges:
            raise ValueError("Cannot remove nonexistent edge.")
        # remove edge from vertices' edge sets
        e.vertices[0]._edges.remove(e)
        e.vertices[1]._edges.remove(e)
        self.edges.remove(e)

    def get_selected(self, mouse_pos: tuple[int, int]) -> Optional[Vertex | Edge]:
        """
        Get the selected (hovered-over) graph element, if such a one exists.

        Vertices have precedence over edges, and the one closest to `mouse_pos`
        is chosen.
        """
        # generate a list of the in-range vertices, sorted by distance
        if in_click_radius := sorted(
            filter(
                lambda v: v.distance_to(mouse_pos) <= VERTEX_HOVER_RADIUS, self.vertices
            ),
            key=lambda v: v.distance_to(mouse_pos),
        ):
            return in_click_radius[0]  # return vertex closest to mouse position

        # generate a list of the in-range edges, sorted by distance
        if in_click_distance := sorted(
            filter(lambda e: e.distance_to(mouse_pos) <= EDGE_HOVER_WIDTH, self.edges),
            key=lambda e: e.distance_to(mouse_pos),
        ):
            return in_click_distance[0]

        return None

    def _dfs(self, v: Vertex, seen: set[Vertex]) -> None:
        """
        Perform a depth-first search starting from `v`.

        Used to determine connectedness.
        """
        if v not in self.vertices:
            raise ValueError("Cannot perform DFS from invalid vertex.")

        # add current vertex to the set of previously-traversed vertices
        seen.add(v)
        for e in v._edges:
            # run DFS from each untraversed neighbor
            if (neighbor := e.walk(v)) not in seen:
                self._dfs(neighbor, seen)
    
    @property
    def connected(self) -> bool:
        """A graph is connected if there is a path between any two of its vertices."""
        
        if len(self.vertices) <= 1:
            return True

        seen: set[Vertex] = set()

        # start with arbitrary vertex
        start = next(iter(self.vertices))
        self._dfs(start, seen)
        
        return len(seen) == len(self.vertices)
    
    @property
    def usable(self) -> tuple[bool, str]:
        """
        A graph is usable for Kruskal's algorithm (in this use case) if it is connected
        and has at least one edge.
        """
        if len(self.edges) == 0:
            return False, "Your graph needs at least one edge!"
        
        if not self.connected:
            return False, "Your graph must be connected!"
        
        return True, "Looks good! Press [ENTER] to run Kruskal's Algorithm!"

    def draw(
        self,
        surf: pg.Surface,
        selected: Optional[Vertex | Edge],
        font: pg.font.Font,
    ) -> None:
        """Draws the graph to the given `Surface`."""
        for e in self.edges:
            if e == selected:
                e.draw(surf, font, EDGE_HOVER_COLOR, EDGE_HOVER_WIDTH)
            else:
                e.draw(surf, font, EDGE_DEFAULT_COLOR, EDGE_DEFAULT_WIDTH)
        for v in self.vertices:
            if v == selected:
                v.draw(surf, VERTEX_HOVER_COLOR, VERTEX_HOVER_RADIUS)
            else:
                v.draw(surf, VERTEX_DEFAULT_COLOR, VERTEX_DEFAULT_RADIUS)


# shorthand for vertex creation
V = lambda x, y: Vertex((x, y))
