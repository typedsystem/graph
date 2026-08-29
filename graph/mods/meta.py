from typed.meta import TYPE
from typed.wrap import closure
from model.meta import MODEL

@closure(lt="__issub__")
class NODE(MODEL):
    pass

@closure(lt="__issub__")
class EDGE(MODEL):
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
        return super().__issub__(other)

    def __call__(met, *args, __origin_cls__=None, __defaults__=None, __extends__=None, **fields):
        if getattr(met, '__is_base_model__', False) or met.__name__ == 'Edge':
            if not fields and not args:
                from typed.mods.types.constructor import Tuple
                from graph.mods.types import Node
                fields = {
                    "__nodes__": Tuple(Node),
                    "__directed__": None,
                    "__order__": -1
                }
            else:
                fields.setdefault("__directed__", getattr(met, "__directed__", None))
                if args:
                    fields["__nodes__"] = list(args)
                elif "__nodes__" not in fields:
                    fields["__nodes__"] = []
                fields["__order__"] = len(fields["__nodes__"])

            return super().__call__(
                __origin_cls__=__origin_cls__,
                __defaults__=__defaults__,
                __extends__=__extends__,
                **fields
            )

        if args:
            fields["__nodes__"] = list(args)
        elif "__nodes__" not in fields:
            fields["__nodes__"] = []
        fields.setdefault("__directed__", getattr(met, "__directed__", None))
        fields["__order__"] = len(fields["__nodes__"])

        return super().__call__(**fields)


@closure(lt="__issub__")
class GRAPH(TYPE):
    import weakref
    __cache__ = weakref.WeakValueDictionary()

    def __isterm__(typ, trm):
        if getattr(typ, '__is_base_graph__', False) or typ.__name__ == 'Graph':
            return (isinstance(trm, type) and issubclass(trm, typ)) or isinstance(trm, typ)
        if isinstance(trm, typ):
            return True
        from typed.mods.check import check
        if not hasattr(trm, "__nodes__") or not hasattr(trm, "__edges__"):
            return False
        cls_nodes = getattr(typ, "__nodes_type__", None)
        if cls_nodes is not None:
            if not check.isterm(getattr(trm, "__nodes__", set()), cls_nodes):
                return False
        cls_edges = getattr(typ, "__edges_type__", None)
        if cls_edges is not None:
            if not check.isterm(getattr(trm, "__edges__", set()), cls_edges):
                return False
        oth_dir = getattr(typ, "__directed__", None)
        if oth_dir is not None:
            if getattr(trm, "__directed__", None) != oth_dir:
                return False
        oth_ord = getattr(typ, "__order__", None)
        if oth_ord is not None:
            if getattr(trm, "__order__", None) != oth_ord:
                return False
        return True

    def __call__(met, *nodes, edge=None, directed=None, order=None, **kwargs):
        if getattr(met, '__is_base_graph__', False) or met.__name__ == 'Graph':
            from typed.mods.init import TYPESYSTEM
            from typed.types import Set
            from graph.mods.types import Node, Edge
            if not nodes and "node" in kwargs:
                nodes = (kwargs["node"],)
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
                __is_base_graph__ = False
            Graph.__name__ = f"{met.__name__}({_nodes.__name__})"
            met.__cache__[cache_key] = Graph
            return Graph
        inst = type.__call__(met)
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

@closure(lt="__issub__")
class DIGRAPH(GRAPH):
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False
        edges = getattr(trm, "__edges__", set())
        return all(getattr(e, "__directed__", False) is True for e in edges)

@closure(lt="__issub__")
class ACYCLIC(GRAPH):
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False
        from graph.mods.prop import prop
        from typed.mods.err import NotDefined
        loops = prop.loopsof(trm)
        if loops is NotDefined:
            return False
        return len(loops) == 0
