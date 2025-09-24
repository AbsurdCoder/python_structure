# graph.py
from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, Hashable, Iterable, List, Optional, Tuple, Set

Vertex = Hashable

@dataclass(frozen=True)
class Edge:
    u: Vertex
    v: Vertex
    weight: float = 1.0

class Graph:
    """
    A simple adjacency-list graph supporting directed/undirected and weighted edges.

    Example:
        g = Graph(directed=False)
        g.add_edge("A", "B", 2)
        g.add_edge("A", "C", 1)
        print(g.bfs("A"))             # ['A','B','C'] (order may vary)
        dist, prev = g.dijkstra("A")  # shortest paths from A
    """
    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        # adjacency[u] = {v: weight, ...}
        self._adj: Dict[Vertex, Dict[Vertex, float]] = defaultdict(dict)

    # ---------- Construction ----------
    def add_vertex(self, v: Vertex) -> None:
        _ = self._adj[v]  # touch to ensure vertex exists

    def add_edge(self, u: Vertex, v: Vertex, weight: float = 1.0) -> None:
        if weight < 0:
            raise ValueError("Edge weight must be non-negative for Dijkstra to work.")
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj[u][v] = weight
        if not self.directed:
            self._adj[v][u] = weight

    def remove_edge(self, u: Vertex, v: Vertex) -> None:
        self._adj[u].pop(v, None)
        if not self.directed:
            self._adj[v].pop(u, None)

    def remove_vertex(self, v: Vertex) -> None:
        self._adj.pop(v, None)
        for nbrs in self._adj.values():
            nbrs.pop(v, None)

    @classmethod
    def from_edges(cls, edges: Iterable[Tuple[Vertex, Vertex, float]], directed: bool = False) -> "Graph":
        g = cls(directed=directed)
        for u, v, w in edges:
            g.add_edge(u, v, w)
        return g

    # ---------- Introspection ----------
    def vertices(self) -> List[Vertex]:
        return list(self._adj.keys())

    def neighbors(self, v: Vertex) -> Dict[Vertex, float]:
        return dict(self._adj.get(v, {}))

    def edges(self) -> List[Edge]:
        out: List[Edge] = []
        for u, nbrs in self._adj.items():
            for v, w in nbrs.items():
                if self.directed or (u <= v):  # avoid duplicates in undirected graphs (order by value)
                    out.append(Edge(u, v, w))
        return out

    def __contains__(self, v: Vertex) -> bool:
        return v in self._adj

    def __len__(self) -> int:
        return len(self._adj)

    def __repr__(self) -> str:
        kind = "DiGraph" if self.directed else "Graph"
        return f"<{kind} | V={len(self._adj)} E={len(self.edges())}>"

    # ---------- Traversals ----------
    def bfs(self, start: Vertex) -> List[Vertex]:
        if start not in self._adj:
            raise KeyError(f"Start vertex {start!r} not in graph.")
        visited: Set[Vertex] = set()
        order: List[Vertex] = []
        q: deque[Vertex] = deque([start])
        visited.add(start)

        while q:
            u = q.popleft()
            order.append(u)
            for v in self._adj[u]:
                if v not in visited:
                    visited.add(v)
                    q.append(v)
        return order

    def dfs(self, start: Vertex) -> List[Vertex]:
        if start not in self._adj:
            raise KeyError(f"Start vertex {start!r} not in graph.")
        visited: Set[Vertex] = set()
        order: List[Vertex] = []

        def _dfs(u: Vertex) -> None:
            visited.add(u)
            order.append(u)
            for v in self._adj[u]:
                if v not in visited:
                    _dfs(v)

        _dfs(start)
        return order

    # ---------- Shortest Paths ----------
    def dijkstra(self, start: Vertex) -> Tuple[Dict[Vertex, float], Dict[Vertex, Optional[Vertex]]]:
        """
        Computes shortest path distances from `start` to all vertices using Dijkstra.
        Returns (dist, prev) where:
          - dist[v] is the distance from start to v (float, inf if unreachable)
          - prev[v] is the predecessor of v on a shortest path (or None for start/unreachable)
        """
        if start not in self._adj:
            raise KeyError(f"Start vertex {start!r} not in graph.")

        import heapq

        dist: Dict[Vertex, float] = {v: float("inf") for v in self._adj}
        prev: Dict[Vertex, Optional[Vertex]] = {v: None for v in self._adj}
        dist[start] = 0.0

        pq: List[Tuple[float, Vertex]] = [(0.0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if d != dist[u]:
                continue  # stale entry
            for v, w in self._adj[u].items():
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))
        return dist, prev

    def reconstruct_path(self, prev: Dict[Vertex, Optional[Vertex]], target: Vertex) -> List[Vertex]:
        """
        Given a predecessor map (from dijkstra), reconstruct the path to `target`.
        Returns empty list if unreachable.
        """
        if target not in prev:
            return []
        path: List[Vertex] = []
        cur: Optional[Vertex] = target
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        # If the path doesn't start at a source (prev[start] is None), ensure it is valid
        return path

    # ---------- DAG Utilities ----------
    def topological_sort(self) -> List[Vertex]:
        """
        Kahn's algorithm. Only valid for directed acyclic graphs (DAG).
        Raises ValueError if the graph has a cycle or is undirected.
        """
        if not self.directed:
            raise ValueError("Topological sort requires a directed graph.")

        indeg: Dict[Vertex, int] = {u: 0 for u in self._adj}
        for u in self._adj:
            for v in self._adj[u]:
                indeg[v] = indeg.get(v, 0) + 1
                # ensure all nodes appear in indeg
                indeg.setdefault(u, indeg.get(u, 0))

        q: deque[Vertex] = deque([u for u, d in indeg.items() if d == 0])
        order: List[Vertex] = []

        while q:
            u = q.popleft()
            order.append(u)
            for v in self._adj.get(u, {}):
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

        if len(order) != len(indeg):
            raise ValueError("Graph has at least one cycle; topological sort not possible.")
        return order

# --------- Demo usage ---------
if __name__ == "__main__":
    # Undirected weighted graph
    g = Graph(directed=False)
    g.add_edge("A", "B", 2)
    g.add_edge("A", "C", 1)
    g.add_edge("B", "D", 5)
    g.add_edge("C", "D", 2)

    print(g)                         # <Graph | V=4 E=4>
    print("Vertices:", g.vertices())
    print("Edges:", g.edges())
    print("BFS from A:", g.bfs("A"))
    print("DFS from A:", g.dfs("A"))
    dist, prev = g.dijkstra("A")
    print("Distances from A:", dist)
    print("Path A->D:", g.reconstruct_path(prev, "D"))

    # Directed DAG example (for topo sort)
    dag = Graph(directed=True)
    dag.add_edge("cook", "eat")
    dag.add_edge("shop", "cook")
    dag.add_edge("plan", "shop")
    print("Topo order (DAG):", dag.topological_sort())
