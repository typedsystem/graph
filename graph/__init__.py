from typed import lazy

__imports__ = {
    "graph.mods.prop": [
        "prop"
    ],
    "graph.mods.checker": [
        "check", "require"
    ],
    "graph.mods.types": [
        "Node",
        "Edge", "Arrow",
        "Graph", "Digraph"
    ]
}

if lazy(__imports__):
    from graph.mods.prop import prop
    from graph.mods.checker import check, require
    from graph.mods.types import (
        Node,
        Edge, Arrow,
        Graph, Digraph
    )
