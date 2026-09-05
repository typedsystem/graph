def _is_loop(entity):
    nodes = getattr(entity, "__nodes__")
    if nodes is None:
        return False
    if getattr(entity, "__arrows__") is not None:
        return len(nodes) > 0 and all(n == nodes[0] for n in nodes)
    if getattr(entity, "__edges__") is not None:
        return len(nodes) == 1
    return False

def _issub(self, other, attr):
    if not hasattr(other, "__nodes__") or not hasattr(other, attr):
        return False
    sub_nodes = getattr(self, "__nodes__", set())
    sup_nodes = getattr(other, "__nodes__", set())
    if not sub_nodes.issubset(sup_nodes):
        return False
    sub_attr = getattr(self, attr, set())
    sup_attr = getattr(other, attr, set())
    return sub_attr.issubset(sup_attr)

def _contains(self, item, attr):
    if item in getattr(self, "__nodes__", set()):
        return True
    return item in getattr(self, attr, set())

class _GraphAdd:
    def __init__(self, graph):
        self.graph = graph

    def node(self, *nodes):
        if not nodes:
            return self.graph
        from typed.mods.check import require
        require.isterm(
            set(nodes),
            self.graph.__class__.__nodes_type__
        )
        self.graph.__nodes__.update(nodes)
        import weakref
        for n in nodes:
            if not hasattr(n, "__graphs__"):
                n.__graphs__ = weakref.WeakKeyDictionary()
            if self.graph not in n.__graphs__:
                n.__graphs__[self.graph] = weakref.WeakSet()
        return self.graph

    def edge(self, *edges):
        if not edges:
            return self.graph
        from typed.mods.check import require
        from typed.mods.err import TypeErr
        require.isterm(
            set(edges),
            self.graph.__class__.__edges_type__
        )
        graph_order = getattr(self.graph.__class__, "__order__", None)
        import weakref
        for e in edges:
            if graph_order is not None:
                e_order = getattr(
                    e,
                    "__order__",
                    len(getattr(e, "__nodes__", []))
                )
                if e_order != graph_order:
                    raise TypeErr(
                        message=f"Graph requires edges of order {graph_order}, but received {e_order}",
                        term=e
                    )
            self.graph.__edges__.add(e)
            if not hasattr(e, "__graphs__"):
                e.__graphs__ = weakref.WeakSet()
            e.__graphs__.add(self.graph)
            e_nodes = getattr(e, '__nodes__', [])
            self.graph.__nodes__.update(e_nodes)
            for n in e_nodes:
                if not hasattr(n, "__graphs__"):
                    n.__graphs__ = weakref.WeakKeyDictionary()
                if self.graph not in n.__graphs__:
                    n.__graphs__[self.graph] = weakref.WeakSet()
                n.__graphs__[self.graph].add(e)
        return self.graph

class _GraphRm:
    def __init__(self, graph):
        self.graph = graph

    def node(self, *nodes):
        if not nodes:
            return self.graph
        nodes_set = set(nodes)
        self.graph.__nodes__.difference_update(nodes_set)
        stale_edges = set()
        for e in self.graph.__edges__:
            e_nodes = getattr(e, "__nodes__", [])
            if any(n in nodes_set for n in e_nodes):
                stale_edges.add(e)
        if stale_edges:
            self.graph.__edges__.difference_update(stale_edges)
        for n in nodes_set:
            graphs = getattr(
                n,
                "__graphs__",
                None
            )
            if graphs is not None:
                graphs.pop(self.graph, None)
        for e in stale_edges:
            graphs = getattr(
                e,
                "__graphs__",
                None
            )
            if graphs is not None:
                graphs.discard(self.graph)
            for n in getattr(e, "__nodes__", []):
                n_graphs = getattr(n, "__graphs__", None)
                if n_graphs is not None and self.graph in n_graphs:
                    n_graphs[self.graph].discard(e)
        return self.graph

    def edge(self, *edges, cleanup=False):
        if not edges:
            return self.graph
        self.graph.__edges__.difference_update(edges)
        for e in edges:
            graphs = getattr(
                e,
                "__graphs__",
                None
            )
            if graphs is not None:
                graphs.discard(self.graph)
            for n in getattr(e, "__nodes__", []):
                n_graphs = getattr(n, "__graphs__", None)
                if n_graphs is not None and self.graph in n_graphs:
                    n_graphs[self.graph].discard(e)
        if cleanup:
            self.graph.cleanup()
        return self.graph

class _DigraphAdd:
    def __init__(self, graph):
        self.graph = graph

    def node(self, *nodes):
        if not nodes:
            return self.graph
        from typed.mods.check import require
        require.isterm(
            set(nodes),
            self.graph.__class__.__nodes_type__
        )
        self.graph.__nodes__.update(nodes)
        import weakref
        for n in nodes:
            if not hasattr(n, "__graphs__"):
                n.__graphs__ = weakref.WeakKeyDictionary()
            if self.graph not in n.__graphs__:
                n.__graphs__[self.graph] = weakref.WeakSet()
        return self.graph

    def arrow(self, *arrows):
        if not arrows:
            return self.graph
        from typed.mods.check import require
        from typed.mods.err import TypeErr
        require.isterm(
            set(arrows),
            self.graph.__class__.__edges_type__
        )
        graph_order = getattr(self.graph.__class__, "__order__", None)
        import weakref
        for a in arrows:
            if graph_order is not None:
                a_order = getattr(
                    a,
                    "__order__",
                    len(getattr(
                        a,
                        "__nodes__",
                        []
                    ))
                )
                if a_order != graph_order:
                    raise TypeErr(
                        message=f"Graph requires arrows of order {graph_order}, but received {a_order}",
                        term=a
                    )
            self.graph.__edges__.add(a)
            if not hasattr(a, "__graphs__"):
                a.__graphs__ = weakref.WeakSet()
            a.__graphs__.add(self.graph)
            a_nodes = getattr(
                a,
                '__nodes__',
                []
            )
            self.graph.__nodes__.update(a_nodes)
            for n in a_nodes:
                if not hasattr(n, "__graphs__"):
                    n.__graphs__ = weakref.WeakKeyDictionary()
                if self.graph not in n.__graphs__:
                    n.__graphs__[self.graph] = weakref.WeakSet()
                n.__graphs__[self.graph].add(a)
        return self.graph

class _DigraphRm:
    def __init__(self, graph):
        self.graph = graph

    def node(self, *nodes):
        if not nodes:
            return self.graph
        nodes_set = set(nodes)
        self.graph.__nodes__.difference_update(nodes_set)
        stale_arrows = set()
        for a in self.graph.__edges__:
            a_nodes = getattr(
                a,
                "__nodes__",
                []
            )
            if any(n in nodes_set for n in a_nodes):
                stale_arrows.add(a)
        if stale_arrows:
            self.graph.__edges__.difference_update(stale_arrows)
        for n in nodes_set:
            graphs = getattr(
                n,
                "__graphs__",
                None
            )
            if graphs is not None:
                graphs.pop(self.graph, None)
        for a in stale_arrows:
            graphs = getattr(
                a,
                "__graphs__",
                None
            )
            if graphs is not None:
                graphs.discard(self.graph)
            for n in getattr(a, "__nodes__", []):
                n_graphs = getattr(n, "__graphs__", None)
                if n_graphs is not None and self.graph in n_graphs:
                    n_graphs[self.graph].discard(a)
        return self.graph

    def arrow(self, *arrows, cleanup=False):
        if not arrows:
            return self.graph
        self.graph.__edges__.difference_update(arrows)
        for a in arrows:
            graphs = getattr(
                a,
                "__graphs__",
                None
            )
            if graphs is not None:
                graphs.discard(self.graph)
            for n in getattr(a, "__nodes__", []):
                n_graphs = getattr(n, "__graphs__", None)
                if n_graphs is not None and self.graph in n_graphs:
                    n_graphs[self.graph].discard(a)
        if cleanup:
            self.graph.cleanup()
        return self.graph
