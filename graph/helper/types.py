class _GraphAdd:
    def __init__(self, graph):
        self.graph = graph

    def node(self, *nodes):
        if not nodes:
            return self.graph

        from typed.mods.check import require
        require.isterm(set(nodes), self.graph.__class__.__nodes_type__)
        self.graph.__nodes__.update(nodes)
        return self.graph

    def edge(self, *edges, directed=None):
        if not edges:
            return self.graph

        from typed.mods.check import require
        from typed.mods.err import TypeErr

        require.isterm(set(edges), self.graph.__class__.__edges_type__)

        graph_order = self.graph.__order__
        graph_directed = self.graph.__directed__

        for e in edges:
            if graph_order is not None:
                e_order = getattr(e, "__order__", len(getattr(e, "__nodes__", [])))
                if e_order != graph_order:
                    raise TypeErr(
                        message=f"Graph requires edges of order {graph_order}, but received {e_order}",
                        term=e
                    )

            is_directed = None
            if graph_directed is not None:
                is_directed = graph_directed
            elif directed is not None:
                is_directed = directed
            else:
                is_directed = getattr(e, "__directed__", None)

            e.__directed__ = is_directed
            self.graph.__edges__.add(e)
            self.graph.__nodes__.update(getattr(e, '__nodes__', []))

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

        return self.graph

    def edge(self, *edges, cleanup=False):
        if not edges:
            return self.graph

        self.graph.__edges__.difference_update(edges)

        if cleanup:
            self.graph.cleanup()

        return self.graph
