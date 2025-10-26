from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from graph import find_nearest_node, bfs, dijkstra, dfs, distance_between_nodes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/path")
def get_path(
    start_lat: float = Query(...),
    start_lon: float = Query(...),
    end_lat: float = Query(...),
    end_lon: float = Query(...),
    algo: str = Query("dijkstra")
):
    start = find_nearest_node((start_lon, start_lat))
    goal = find_nearest_node((end_lon, end_lat))

    if algo == "bfs":
        path = bfs(start, goal)
        if path:
            dist = sum(distance_between_nodes(path[i], path[i+1]) for i in range(len(path)-1))
    elif algo == "dfs":
        path = dfs(start, goal)
        if path:
            dist = sum(distance_between_nodes(path[i], path[i+1]) for i in range(len(path)-1))
    else: 
        path, dist = dijkstra(start, goal)
        if path:
            dist = sum(distance_between_nodes(path[i], path[i+1]) for i in range(len(path)-1))

    if not path:
        return {"error": "No path found"}

    return {
        "algorithm": algo,
        "distance": dist,
        "path": [{"lat": p[1], "lon": p[0]} for p in path]
    }
