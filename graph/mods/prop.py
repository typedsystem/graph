class prop:
    @staticmethod
    def nodesof(entity, edge=None):
        from typed.mods.err import NotDefined
        if edge is None:
            nodes = getattr(entity, "__nodes__", NotDefined)
            if nodes is not NotDefined:
                return nodes
            return NotDefined
        edges = getattr(entity, "__edges__", NotDefined)
        if edges is not NotDefined and edge not in edges:
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="Edge not found in graph",
                term=edge,
                expected="Edge in graph"
            )
        if edges is not NotDefined:
            return getattr(edge, "__nodes__", [])
        return NotDefined

    @staticmethod
    def edgesof(entity, node=None):
        from typed.mods.err import NotDefined
        if node is None:
            edges = getattr(entity, "__edges__", NotDefined)
            if edges is not NotDefined:
                return edges
            return NotDefined
        nodes = getattr(entity, "__nodes__", NotDefined)
        if nodes is not NotDefined and node not in nodes:
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="Node not found in graph",
                term=node,
                expected="Node in graph"
            )
        edges = getattr(entity, "__edges__", NotDefined)
        if edges is not NotDefined:
            return {e for e in edges if node in getattr(e, "__nodes__", [])}
        return NotDefined

    @staticmethod
    def graphsof(entity):
        from typed import NotDefined
        graphs = getattr(entity, "__graphs__", NotDefined)
        return set(graphs) if graphs is not NotDefined else graphs

    @staticmethod
    def orderof(entity):
        from typed.mods.err import NotDefined
        edges = getattr(entity, "__edges__", NotDefined)
        if edges is not NotDefined:
            nodes = getattr(entity, "__nodes__", NotDefined)
            if nodes is not NotDefined:
                return len(nodes)
        order = getattr(entity, "__order__", NotDefined)
        if order is not NotDefined:
            return order
        return NotDefined

    @staticmethod
    def sizeof(entity):
        from typed.mods.err import NotDefined
        nodes = getattr(entity, "__nodes__", NotDefined)
        edges = getattr(entity, "__edges__", NotDefined)
        if nodes is not NotDefined and edges is not NotDefined:
            return len(nodes) + len(edges)
        return NotDefined

    @staticmethod
    def degreeof(entity, *nodes):
        from typed.mods.err import NotDefined
        graph_nodes = getattr(entity, "__nodes__", NotDefined)
        nodes_set = set(nodes)
        if graph_nodes is not NotDefined and not nodes_set.issubset(graph_nodes):
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="One or more nodes not found in graph",
                term=nodes,
                expected="Nodes in graph"
            )
        if len(nodes_set) == 1:
            degs = getattr(entity, "__degrees__", None)
            if degs is None:
                from graph.helper.prop import _build_degrees
                degs = _build_degrees(entity)
            if degs is not NotDefined:
                return degs.get(next(iter(nodes_set)), 0)
        edges = getattr(entity, "__edges__", NotDefined)
        if edges is not NotDefined:
            count = 0
            for e in edges:
                if nodes_set.issubset(getattr(e, "__nodes__", [])):
                    count += 1
            return count
        return NotDefined

    @staticmethod
    def loopsof(entity):
        from typed.mods.err import NotDefined
        edges = getattr(entity, "__edges__", NotDefined)
        if edges is not NotDefined:
            return {e for e in edges if len(set(getattr(e, "__nodes__", []))) == 1}
        return NotDefined

    @staticmethod
    def neighboorsof(entity, node):
        from typed.mods.err import NotDefined
        nodes = getattr(entity, "__nodes__", NotDefined)
        if nodes is not NotDefined:
            return NotDefined
        if node not in nodes:
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="Node not found in graph",
                term=node,
                expected="Node in graph"
            )
        adj = getattr(entity, "__adjacency__", None)
        if adj is None:
            from graph.helper.prop import _build_adjacency
            adj = _build_adjacency(entity)
            if adj is NotDefined:
                return NotDefined
        return set(adj.get(node, set()))

    @staticmethod
    def orphansof(entity):
        from typed.mods.err import NotDefined
        adj = getattr(entity, "__adjacency__", None)
        if adj is None:
            from graph.helper.prop import _build_adjacency
            adj = _build_adjacency(entity)
            if adj is NotDefined:
                return NotDefined
        return {n for n, neighbors in adj.items() if not neighbors}

    @staticmethod
    def compof(entity, item):
        from typed.mods.err import NotDefined
        from typed.mods.err import TypeErr
        nodes = getattr(entity, "__nodes__", NotDefined)
        if nodes is NotDefined:
            return NotDefined
        if hasattr(item, "__nodes__"):
            edges = getattr(entity, "__edges__", NotDefined)
            if edges is not NotDefined and item not in edges:
                raise TypeErr(
                    message="Edge not found in graph",
                    term=item,
                    expected="Edge in graph"
                )
            start_nodes = getattr(item, "__nodes__", [])
        else:
            if item not in nodes:
                raise TypeErr(
                    message="Node not found in graph",
                    term=item,
                    expected="Node in graph"
                )
            start_nodes = [item]
        comps = getattr(entity, "__components__", None)
        if comps is not None:
            start_set = set(start_nodes)
            for comp in comps:
                comp_nodes = getattr(comp, "__nodes__", set())
                if start_set.issubset(comp_nodes):
                    return comp
            return NotDefined
        if not start_nodes:
            return entity.induced()
        comp_nodes = set()
        from graph.mods.func import traverse, induced
        for curr, _ in traverse(
            entity,
            start=start_nodes[0],
            mode="dfs"
        ):
            comp_nodes.add(curr)
        return induced(entity, *comp_nodes)

    @staticmethod
    def compsof(entity):
        from typed.mods.err import NotDefined
        comps = getattr(entity, "__components__", None)
        if comps is not None:
            for comp in comps:
                yield comp
            return
        nodes = getattr(entity, "__nodes__", NotDefined)
        if nodes is NotDefined:
            return
        visited = set()
        components = []
        from graph.mods.func import traverse, induced
        for n in nodes:
            if n not in visited:
                comp_nodes = set()
                for curr, _ in traverse(
                    entity,
                    start=n,
                    mode="dfs"
                ):
                    comp_nodes.add(curr)
                visited.update(comp_nodes)
                comp = induced(entity, *comp_nodes)
                components.append(comp)
                yield comp
        entity.__components__ = components
