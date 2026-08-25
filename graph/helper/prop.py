def _build_adjacency(entity):
    from typed import NotDefined
    import weakref
    edges = getattr(entity, "__edges__", NotDefined)
    nodes = getattr(entity, "__nodes__", NotDefined)

    if edges is NotDefined or nodes is NotDefined:
        return NotDefined

    try:
        adj = weakref.WeakKeyDictionary()
        for n in nodes:
            adj[n] = set()
    except TypeError:
        adj = {n: set() for n in nodes}

    for e in edges:
        e_nodes = getattr(e, "__nodes__", [])
        for n in e_nodes:
            if n not in adj:
                adj[n] = set()
            adj[n].update(e_nodes)
    entity.__adjacency__ = adj
    return adj

def _build_degrees(entity):
    from typed import NotDefined
    import weakref
    edges = getattr(entity, "__edges__", NotDefined)
    nodes = getattr(entity, "__nodes__", NotDefined)

    if edges is NotDefined or nodes is NotDefined:
        return NotDefined

    try:
        degs = weakref.WeakKeyDictionary()
        for n in nodes:
            degs[n] = 0
    except TypeError:
        degs = {n: 0 for n in nodes}

    for e in edges:
        for n in getattr(e, "__nodes__", []):
            degs[n] = degs.get(n, 0) + 1
    entity.__degrees__ = degs
    return degs
