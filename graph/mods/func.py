def induced(
    graph,
    *elements,
    exclude: bool=False,
    freeze: bool=False
):
    is_digraph = hasattr(graph, "arrowsof")
    explicit_nodes = set()
    explicit_edges = set()
    from graph.mods.checker import check
    from typed.mods.err import TypeErr

    for el in elements:
        if hasattr(el, "__nodes__"):
            if is_digraph and not check.arrow.isarrow(el):
                raise TypeErr(
                    message="Digraph expects arrows",
                    term=el,
                    expected="Arrow"
                )
            if not is_digraph and not check.edge.isedge(el):
                raise TypeErr(
                    message="Graph expects edges",
                    term=el,
                    expected="Edge"
                )
            explicit_edges.add(el)
        else:
            explicit_nodes.add(el)

    subgraph = graph.__class__()
    edges_to_add = set()

    if not exclude:
        if not explicit_nodes.issubset(graph.__nodes__):
            raise TypeErr(
                message="One or more nodes not found in graph",
                term=elements
            )
        if not explicit_edges.issubset(graph.__edges__):
            raise TypeErr(
                message="One or more edges/arrows not found in graph",
                term=elements
            )

        nodes_set = set(explicit_nodes)
        for e in explicit_edges:
            nodes_set.update(getattr(e, "__nodes__", []))

        subgraph.add.node(*nodes_set)

        for e in graph.__edges__:
            if e in explicit_edges or set(getattr(e, "__nodes__", [])).issubset(nodes_set):
                edges_to_add.add(e)
    else:
        nodes_set = graph.__nodes__ - explicit_nodes
        subgraph.add.node(*nodes_set)

        for e in graph.__edges__:
            if e not in explicit_edges and set(getattr(e, "__nodes__", [])).issubset(nodes_set):
                edges_to_add.add(e)

    if is_digraph:
        subgraph.add.arrow(*edges_to_add)
    else:
        subgraph.add.edge(*edges_to_add)

    if freeze:
        subgraph.__frozen__ = True
    return subgraph


def spanning(
    graph,
    *elements,
    exclude: bool=False,
    freeze: bool=False
):
    is_digraph = hasattr(graph, "arrowsof")
    explicit_nodes = set()
    explicit_edges = set()
    from graph.mods.checker import check
    from typed.mods.err import TypeErr

    for el in elements:
        if hasattr(el, "__nodes__"):
            if is_digraph and not check.arrow.isarrow(el):
                raise TypeErr(
                    message="Digraph expects arrows",
                    term=el,
                    expected="Arrow"
                )
            if not is_digraph and not check.edge.isedge(el):
                raise TypeErr(
                    message="Graph expects edges",
                    term=el,
                    expected="Edge"
                )
            explicit_edges.add(el)
        else:
            explicit_nodes.add(el)

    subgraph = graph.__class__()
    subgraph.add.node(*graph.__nodes__)
    edges_to_add = set()

    if not exclude:
        if not explicit_nodes.issubset(graph.__nodes__):
            raise TypeErr(
                message="One or more nodes not found in graph",
                term=elements
            )
        if not explicit_edges.issubset(graph.__edges__):
            raise TypeErr(
                message="One or more edges/arrows not found in graph",
                term=elements
            )

        if not explicit_nodes:
            edges_to_add.update(explicit_edges)
        else:
            for e in graph.__edges__:
                if e in explicit_edges or set(getattr(e, "__nodes__", [])).issubset(explicit_nodes):
                    edges_to_add.add(e)
    else:
        if not explicit_nodes:
            edges_to_add.update(graph.__edges__ - explicit_edges)
        else:
            for e in graph.__edges__:
                if e not in explicit_edges and not set(getattr(e, "__nodes__", [])).issubset(explicit_nodes):
                    edges_to_add.add(e)

    if is_digraph:
        subgraph.add.arrow(*edges_to_add)
    else:
        subgraph.add.edge(*edges_to_add)

    if freeze:
        subgraph.__frozen__ = True
    return subgraph

def traverse(
    graph,
    start=None,
    mode="dfs",
    node_filters=None,
    edge_filters=None
):
    from typed.mods.err import NotDefined, TypeErr
    from graph.mods.prop import prop

    nodes = prop.nodesof(entity=graph)
    if nodes is NotDefined:
        return

    if node_filters is not None:
        if callable(node_filters):
            node_filters = (node_filters,)
    else:
        node_filters = ()

    if edge_filters is not None:
        if callable(edge_filters):
            edge_filters = (edge_filters,)
    else:
        edge_filters = ()

    if start is not None:
        if start not in nodes:
            raise TypeErr(
                message="Start node not found in graph",
                term=start,
                expected="Node in graph"
            )
        if node_filters and not all(f(start) for f in node_filters):
            return
        start_nodes = [start]
    else:
        if node_filters:
            start_nodes = [n for n in nodes if all(f(n) for f in node_filters)]
        else:
            start_nodes = list(nodes)

    if mode == "bfs":
        import collections
        frontier = collections.deque()
        push = frontier.append
        pop = frontier.popleft
    elif mode == "dfs":
        frontier = []
        push = frontier.append
        pop = frontier.pop
    else:
        raise TypeErr(
            message="Invalid traversal mode",
            term=mode,
            expected="'dfs' or 'bfs'"
        )

    visited = set()
    is_digraph = hasattr(graph, "arrowsof")

    for root in start_nodes:
        if root in visited:
            continue
        push(root)
        while frontier:
            curr = pop()
            if curr in visited:
                continue
            visited.add(curr)

            neighbors = []
            graphs = getattr(curr, "__graphs__", None)
            if graphs is not None and graph in graphs:
                for e in graphs[graph]:
                    if edge_filters and not all(f(e) for f in edge_filters):
                        continue

                    e_nodes = getattr(e, "__nodes__", [])
                    if is_digraph or isinstance(e_nodes, list):
                        e_nodes_list = list(e_nodes)
                        if e_nodes_list and e_nodes_list[0] == curr:
                            for n in e_nodes_list[1:]:
                                if n not in visited:
                                    if not node_filters or all(f(n) for f in node_filters):
                                        neighbors.append(n)
                    else:
                        for n in e_nodes:
                            if n != curr and n not in visited:
                                if not node_filters or all(f(n) for f in node_filters):
                                    neighbors.append(n)

            unique_neighbors = list(dict.fromkeys(neighbors))
            yield curr, unique_neighbors

            if mode == "dfs":
                for neighbor in reversed(unique_neighbors):
                    if neighbor not in visited:
                        push(neighbor)
            else:
                for neighbor in unique_neighbors:
                    if neighbor not in visited:
                        push(neighbor)
