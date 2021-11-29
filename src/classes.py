# classes for graph modeling
from constants import *


class Vertex:
    """Represents a vertex with positional information."""

    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos = pos

    def draw(self) -> None:
        pass


class Edge:
    """Represents a weighted edge."""

    def __init__(self, a: Vertex, b: Vertex, weight: int) -> None:
        self.vertices = (a, b)
        self.weight = weight

    def draw(self) -> None:
        pass


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

    def draw(self) -> None:
        pass


# shorthand for vertex creation
V = lambda x, y: Vertex((x, y))
