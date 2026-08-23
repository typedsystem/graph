from typed import lazy

__imports__ = {
    "graph.mods.err": [
        "NodeErr",
        "EdgeErr", "ArrowErr",
        "GraphErr", "DigraphErr"
    ]
}

if lazy(__imports__):
    from graph.mods.err import (
        NodeErr,
        EdgeErr, ArrowErr,
        GraphErr, DigraphErr
    )
