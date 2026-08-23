from typed.meta import TYPE

class NODE(TYPE):
    def __call__(met, **kwargs):
        if not kwargs:
            return TYPE
        if getattr(met, '__is_base_model__', False):
            class Node(met, metaclass=NODE):
                __typesystems__ = met.__typesystems__
            for k, v in kwargs.items():
                setattr(Node, k, v)
            return Node
        inst = super().__call__()
        for k, v in kwargs.items():
            setattr(inst, k, v)
        return inst

class EDGE(TYPE):
    def __issub__(cls, other):
        if not isinstance(other, EDGE):
            return False

        oth_dir = getattr(other, "__directed__", None)
        if oth_dir is not None:
            if getattr(cls, "__directed__", None) != oth_dir:
                return False

        oth_ord = getattr(other, "__order__", None)
        if oth_ord is not None:
            if getattr(cls, "__order__", None) != oth_ord:
                return False

        return True

    def __call__(met, *args, **kwargs):
        if getattr(met, '__is_base_model__', False) or met.__name__ == 'Edge':
            if not kwargs and not args:
                from typed.types import Set
                from graph.mods.types import Node
                return super().__call__(
                    __nodes__=Set(Node),
                    __directed__=None,
                    __order__=-1
                )
            class Edge(met, metaclass=EDGE):
                __typesystems__ = met.__typesystems__
            for k, v in kwargs.items():
                setattr(Edge, k, v)
            return Edge

        if args:
            kwargs["__nodes__"] = list(args)
        elif "__nodes__" not in kwargs:
            kwargs["__nodes__"] = []

        kwargs.setdefault("__directed__", getattr(met, "__directed__", None))
        kwargs["__order__"] = len(kwargs["__nodes__"])

        inst = super().__call__()
        for k, v in kwargs.items():
            setattr(inst, k, v)
        return inst

class GRAPH(TYPE):
    import weakref
    __cache__ = weakref.WeakValueDictionary()

    def __issub__(cls, other):
        if not isinstance(other, GRAPH):
            return False

        from typed.mods.check import check

        oth_nodes = getattr(other, "__nodes_type__", None)
        if oth_nodes is not None:
            cls_nodes = getattr(cls, "__nodes_type__", None)
            if cls_nodes is None or not check.issub(cls_nodes, oth_nodes):
                return False

        oth_edges = getattr(other, "__edges_type__", None)
        if oth_edges is not None:
            cls_edges = getattr(cls, "__edges_type__", None)
            if cls_edges is None or not check.issub(cls_edges, oth_edges):
                return False

        oth_dir = getattr(other, "__directed__", None)
        if oth_dir is not None:
            if getattr(cls, "__directed__", None) != oth_dir:
                return False

        oth_ord = getattr(other, "__order__", None)
        if oth_ord is not None:
            if getattr(cls, "__order__", None) != oth_ord:
                return False

        return True

    def __call__(met, *nodes, edge=None, directed=None, order=None, **kwargs):
        if getattr(met, '__is_base_graph__', False) or met.__name__ == 'Graph':
            from typed.mods.init import TYPESYSTEM
            from typed.types import Set
            from graph.mods.types import Node, Edge

            _nodes = Set(*nodes) if nodes else Set(Node)
            _edges = Set(edge) if edge else Set(Edge)

            cache_key = (met, _nodes, _edges, directed, order)
            if cache_key in met.__cache__:
                return met.__cache__[cache_key]

            class Graph(met, metaclass=GRAPH):
                __typesystems__ = {TYPESYSTEM}
                __nodes_type__ = _nodes
                __edges_type__ = _edges
                __directed__ = directed
                __order__ = order

            Graph.__name__ = f"{met.__name__}({_nodes.__name__})"
            met.__cache__[cache_key] = Graph
            return Graph

        inst = super().__call__()
        inst_nodes = kwargs.get("nodes", set())
        inst_edges = kwargs.get("edges", set())

        if not inst_nodes and inst_edges:
            inferred = set()
            for e in inst_edges:
                inferred.update(getattr(e, "__nodes__", []))
            inst_nodes = inferred

        inst.__nodes__ = inst_nodes
        inst.__edges__ = set()
        inst.__directed__ = getattr(met, "__directed__", directed)
        inst.__order__ = getattr(met, "__order__", order)

        for e in inst_edges:
            inst.add.edge(e)

        return inst
