class prop:
    @staticmethod
    def nodesof(entity):
        from typed import NotDefined
        return getattr(entity, "__nodes__", NotDefined)

    @staticmethod
    def edgesof(entity):
        from typed import NotDefined
        return getattr(entity, "__edges__", NotDefined)

    @staticmethod
    def graphsof(entity):
        from typed import NotDefined
        graphs = getattr(entity, "__graphs__", NotDefined)
        return set(graphs.keys()) if graphs is not NotDefined else graphs

    @staticmethod
    def arrowsof(entity):
        from typed import NotDefined
        return getattr(entity, "__nodes__", NotDefined)

    @staticmethod
    def loopsof(entity):
        from graph.helper.prop import _loopsof
        if hasattr(entity, "__edges__"):
            return _loopsof(entity, "__edges__")
        if hasattr(entity, "__arrows__"):
            return _loopsof(entity, "__arrows__")
        from typed import NotDefined
        return NotDefined

    @staticmethod
    def orderof(entity):
        from typed import NotDefined
        return getattr(entity, "__order__", NotDefined)

    @staticmethod
    def neighboorsof(entity, node):
        from typed.mods.err import NotDefined, TypeErr
        nodes = getattr(entity, "__nodes__", NotDefined)
        if nodes is not NotDefined and node not in nodes:
            raise TypeErr(
                message="Node not found in graph",
                term=node,
                expected="Node in graph"
            )
        graphs = getattr(node, "__graphs__", None)
        if graphs is not None and entity in graphs:
            neighbors = set()
            is_digraph = hasattr(entity, "arrowsof")
            for e in graphs[entity]:
                e_nodes = getattr(e, "__nodes__", [])
                if is_digraph or isinstance(e_nodes, list):
                    e_nodes_list = list(e_nodes)
                    if e_nodes_list and e_nodes_list[0] == node:
                        for n in e_nodes_list[1:]:
                            neighbors.add(n)
                else:
                    for n in e_nodes:
                        if n != node:
                            neighbors.add(n)
                        elif len(e_nodes) == 1 or (isinstance(e_nodes, (list, tuple)) and e_nodes.count(node) > 1):
                            neighbors.add(n)
            return neighbors
        return set()

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
        if not nodes_set:
            return NotDefined
        if len(nodes_set) == 1:
            n = next(iter(nodes_set))
            return len(prop.neighboorsof(entity=entity, node=n))
        neighbors_list = [prop.neighboorsof(entity=entity, node=n) for n in nodes_set]
        return len(set.intersection(*neighbors_list))

    @staticmethod
    def orphansof(entity):
        from typed import NotDefined
        from graph.mods.checker import check
        nodes = getattr(entity, "__nodes__", NotDefined)
        return nodes if nodes is NotDefined else {n for n in nodes if check.node.isorphan(n, entity)} 

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
        visited = set()
        frontier = list(start_nodes)
        while frontier:
            curr = frontier.pop()
            if curr not in visited:
                visited.add(curr)
                comp_nodes.add(curr)
                graphs = getattr(curr, "__graphs__", None)
                if graphs is not None and entity in graphs:
                    for e in graphs[entity]:
                        for neighbor in getattr(e, "__nodes__", []):
                            if neighbor not in visited:
                                frontier.append(neighbor)

        from graph.mods.func import induced
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
        from graph.mods.func import induced
        for n in nodes:
            if n not in visited:
                comp_nodes = set()
                frontier = [n]
                while frontier:
                    curr = frontier.pop()
                    if curr not in visited:
                        visited.add(curr)
                        comp_nodes.add(curr)
                        graphs = getattr(curr, "__graphs__", None)
                        if graphs is not None and entity in graphs:
                            for e in graphs[entity]:
                                for neighbor in getattr(e, "__nodes__", []):
                                    if neighbor not in visited:
                                        frontier.append(neighbor)

                comp = induced(entity, *comp_nodes)
                components.append(comp)
                yield comp
        entity.__components__ = components
