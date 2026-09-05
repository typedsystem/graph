def _sizeof(self, attr):
    return len(getattr(self, "__nodes__", set())) + len(getattr(self, attr, set()))

def _loopsof(self, attr):
    return {e for e in getattr(self, attr, set()) if len(set(getattr(e, "__nodes__", []))) == 1}

def _adjacency(entity, attr):
    from typed.mods.err import NotDefined
    from graph.mods.prop import prop
    import weakref

    nodes = getattr(entity, "__nodes__", NotDefined)
    if nodes is NotDefined:
        return NotDefined

    adj = weakref.WeakKeyDictionary()
    for n in nodes:
        adj[n] = prop.neighboorsof(entity, n)

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
