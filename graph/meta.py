from typed import lazy

__imports__ = {
    "graph.mods.meta": [
        "NODE", "EDGE", "GRAPH",
        "ACYCLIC", "DIGRAPH"
    ]
}

if lazy(__imports__):
    from graph.mods.meta import (
        NODE, EDGE, GRAPH,
        ACYCLIC, DIGRAPH
    )
