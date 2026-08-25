from typed import lazy

__imports__ = {
    "graph.mods.types": [
        "Node", "Edge",
        "Graph", "Digraph", "Acyclic"
    ]
}

if lazy(__imports__):
    from graph.mods.types import (
        Node, Edge,
        Graph, Digraph, Acyclic
    )
