import heapq
from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.vertices = set()
    
    def add_edge(self, u, v, weight):
        """Add an edge to the graph"""
        self.graph[u].append((v, weight))
        self.vertices.add(u)
        self.vertices.add(v)
    
    def dijkstra(self, src):
        """
        Dijkstra's algorithm using min-heap
        Returns distances from src to all vertices
        """
        # Initialize distances dictionary
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[src] = 0
        
        # Min-heap: (distance, vertex)
        heap = [(0, src)]
        visited = set()
        parent = {vertex: None for vertex in self.vertices}
        
        while heap:
            current_dist, current_vertex = heapq.heappop(heap)
            
            # Skip if already visited
            if current_vertex in visited:
                continue
            
            visited.add(current_vertex)
            
            # Check if current distance is outdated
            if current_dist > distances[current_vertex]:
                continue
            
            # Update distances to neighbors
            for neighbor, weight in self.graph[current_vertex]:
                distance = current_dist + weight
                
                # If a shorter path is found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    parent[neighbor] = current_vertex
                    heapq.heappush(heap, (distance, neighbor))
        
        return distances, parent
    
    def print_distances(self, src):
        """Print shortest distances from source vertex"""
        distances, parent = self.dijkstra(src)
        
        print(f"Dijkstra's Algorithm - Python Implementation")
        print("=" * 50)
        print(f"\nShortest distances from vertex {src}:\n")
        print(f"{'Vertex':<10} {'Distance':<15} {'Path':<20}")
        print("-" * 45)
        
        for vertex in sorted(distances.keys()):
            dist = distances[vertex]
            dist_str = str(dist) if dist != float('inf') else "INF"
            
            # Reconstruct path
            path = []
            current = vertex
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            path_str = " -> ".join(map(str, path)) if dist != float('inf') else "N/A"
            
            print(f"{vertex:<10} {dist_str:<15} {path_str:<20}")


# Example usage
if __name__ == "__main__":
    g = Graph()
    
    # Add edges (source, destination, weight)
    edges = [
        (0, 1, 4), (0, 2, 2),
        (1, 2, 1), (1, 3, 5),
        (2, 3, 8), (2, 4, 10),
        (3, 4, 2), (3, 5, 6),
        (4, 5, 3)
    ]
    
    for u, v, w in edges:
        g.add_edge(u, v, w)
    
    # Run Dijkstra from vertex 0
    g.print_distances(0)
    
    print("\n" + "=" * 50)
    print("\nShortest distances from vertex 2:\n")
    g.print_distances(2)