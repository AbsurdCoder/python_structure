flowchart TD

    subgraph Construction
        A[Start] --> B[Add Vertex]
        B --> C[Add Edge]
        C -->|Directed/Undirected| D{Graph Type}
        D -->|Undirected| E[Mirror Edge u<-->v]
        D -->|Directed| F[Store Edge u->v]
    end

    subgraph Traversals
        G[BFS] --> H[Queue Initialization]
        H --> I[Visit Neighbors]
        I --> J[Traverse All Vertices]

        K[DFS] --> L[Recursive Visit]
        L --> M[Explore Neighbors Recursively]
    end

    subgraph ShortestPaths
        N[Dijkstra] --> O[Initialize Distances & Prev]
        O --> P[Priority Queue Pop]
        P --> Q[Relax Neighbor Distances]
        Q --> P
        P --> R[Done -> Dist + Prev Maps]
    end

    subgraph DAG
        S[Topological Sort] --> T[Compute In-Degree]
        T --> U[Queue Zero In-Degree]
        U --> V[Process Vertices in Order]
        V --> W[Detect Cycle or Output Order]
    end

    Construction --> Traversals
    Construction --> ShortestPaths
    Construction --> DAG
