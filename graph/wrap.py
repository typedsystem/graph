from typed import lazy

__imports__ = {
    "graph.mods.wrap": [
        "node", "edge"
    ]
}

if lazy(__imports__):
    from graph.mods.wrap import node, edge
