from typed import lazy

__imports__ = {
    "graph.mods.types": [
        "Node",
        "Edge", "Arrow",
        "Graph", "Digraph"
    ]
}

if lazy(__imports__):
    from graph.mods.types import (
        Node,
        Edge, Arrow,
        Graph, Digraph
    )
