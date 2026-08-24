from typed import lazy

__imports__ = {
    "graph.mods.prop": [
        "prop"
    ],
    "graph.checker": [
        "check", "require"
    ],
    "graph.types": [
        "Node",
        "Edge", "Arrow",
        "Graph", "Digraph"
    ],
    "graph.wrap": [
        "node", "edge"
    ]
}

if lazy(__imports__):
    from graph.mods.prop import prop
    from graph.checker import check, require
    from graph.types import (
        Node,
        Edge, Arrow,
        Graph, Digraph
    )
    from graph.wrap import node, edge
