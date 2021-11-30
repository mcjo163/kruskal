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

    def distance_to(self, point: tuple[int, int]) -> float:
        """Returns the distance from this vertex to a given point."""
        return pt_distance(self.pos, point)

    def draw(self, surf: pg.Surface, color: tuple[int, int, int], radius: int) -> None:
        """Draws the vertex to the given `Surface`."""
        pg.draw.circle(surf, color, self.pos, radius)


class Edge:
    """Represents a weighted edge."""

    def __init__(self, a: Vertex, b: Vertex, weight: int) -> None:
        self.vertices = (a, b)
        self.weight = weight

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

    def draw(self, surf: pg.Surface, color: tuple[int, int, int], width: int) -> None:
        """Draws the edge to the given `Surface`."""
        a, b = self.vertices

        # attempt to normalize line thickness
        diff = (abs(a.pos[0] - b.pos[0]), abs(a.pos[1] - b.pos[1]))
        t = int(min(diff) / max(diff) + (width / 1.5))

        pg.draw.line(surf, color, a.pos, b.pos, width=width+t)


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
            filter(
                lambda e: e.distance_to(mouse_pos) <= EDGE_HOVER_WIDTH, self.edges
            ),
            key=lambda e: e.distance_to(mouse_pos),
        ):
            return in_click_distance[0]

        return None

    def draw(
        self,
        surf: pg.Surface,
        selected: Optional[Vertex | Edge],
    ) -> None:
        """Draws the graph to the given `Surface`."""
        for e in self.edges:
            if e == selected:
                e.draw(surf, EDGE_HOVER_COLOR, EDGE_HOVER_WIDTH)
            else:
                e.draw(surf, EDGE_DEFAULT_COLOR, EDGE_DEFAULT_WIDTH)
        for v in self.vertices:
            if v == selected:
                v.draw(surf, VERTEX_HOVER_COLOR, VERTEX_HOVER_RADIUS)
            else:
                v.draw(surf, VERTEX_DEFAULT_COLOR, VERTEX_DEFAULT_RADIUS)


# shorthand for vertex creation
V = lambda x, y: Vertex((x, y))
