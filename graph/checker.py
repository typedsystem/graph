from typed import lazy

__imports__ = {
    "graph.mods.checker": [
        "GraphChecker",
        "check", "require"
    ]
}

if lazy(__imports__):
    from graph.mods.checker import (
        GraphChecker,
        check, require
    )
