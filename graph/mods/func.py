def induced(graph, *elements, exclude: bool = False, freeze: bool = False):
    explicit_nodes = set()
    explicit_edges = set()
    for el in elements:
        if hasattr(el, "__nodes__"):
            explicit_edges.add(el)
        else:
            explicit_nodes.add(el)

    subgraph = graph.__class__()

    if not exclude:
        if not explicit_nodes.issubset(graph.__nodes__):
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="One or more nodes not found in graph",
                term=elements
            )
        if not explicit_edges.issubset(graph.__edges__):
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="One or more edges not found in graph",
                term=elements
            )

        nodes_set = set(explicit_nodes)
        for e in explicit_edges:
            nodes_set.update(getattr(e, "__nodes__", []))

        subgraph.__nodes__.update(nodes_set)
        for e in graph.__edges__:
            if e in explicit_edges or set(getattr(e, "__nodes__", [])).issubset(nodes_set):
                subgraph.__edges__.add(e)
    else:
        nodes_set = graph.__nodes__ - explicit_nodes
        subgraph.__nodes__.update(nodes_set)
        for e in graph.__edges__:
            if e not in explicit_edges and set(getattr(e, "__nodes__", [])).issubset(nodes_set):
                subgraph.__edges__.add(e)

    if freeze:
        subgraph.__frozen__ = True

    return subgraph

def spanning(graph, *elements, exclude: bool = False, freeze: bool = False):
    explicit_nodes = set()
    explicit_edges = set()
    for el in elements:
        if hasattr(el, "__nodes__"):
            explicit_edges.add(el)
        else:
            explicit_nodes.add(el)

    subgraph = graph.__class__()
    subgraph.__nodes__.update(graph.__nodes__)

    if not exclude:
        if not explicit_nodes.issubset(graph.__nodes__):
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="One or more nodes not found in graph",
                term=elements
            )
        if not explicit_edges.issubset(graph.__edges__):
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="One or more edges not found in graph",
                term=elements
            )

        if not explicit_nodes:
            subgraph.__edges__.update(explicit_edges)
        else:
            for e in graph.__edges__:
                if e in explicit_edges or set(getattr(e, "__nodes__", [])).issubset(explicit_nodes):
                    subgraph.__edges__.add(e)
    else:
        if not explicit_nodes:
            subgraph.__edges__.update(graph.__edges__ - explicit_edges)
        else:
            for e in graph.__edges__:
                if e not in explicit_edges and not set(getattr(e, "__nodes__", [])).issubset(explicit_nodes):
                    subgraph.__edges__.add(e)

    if freeze:
        subgraph.__frozen__ = True

    return subgraph

def traverse(graph, start=None, mode="dfs"):
    from typed.mods.err import NotDefined, TypeErr
    from graph.mods.prop import prop

    nodes = prop.nodesof(entity=graph)
    if nodes is NotDefined:
        return

    if start is not None:
        if start not in nodes:
            raise TypeErr(
                message="Start node not found in graph",
                term=start,
                expected="Node in graph"
            )
        start_nodes = [start]
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
    for root in start_nodes:
        if root in visited:
            continue
        push(root)
        while frontier:
            curr = pop()
            if curr not in visited:
                visited.add(curr)
                neighbors = list(prop.neighboorsof(entity=graph, node=curr) - visited)
                yield curr, neighbors

                if mode == "dfs":
                    for neighbor in reversed(neighbors):
                        if neighbor not in visited:
                            push(neighbor)
                else:
                    for neighbor in neighbors:
                        if neighbor not in visited:
                            push(neighbor)
