from typed import Union, Filtered, prop
from model import Model
from graph.mods.meta import NODE, EDGE, ARROW, GRAPH, DIGRAPH
from graph.helper.types import _is_loop

class Node(Model, metaclass=NODE):
    __is_base_model__ = True

    def graphsof(self):
        return set(getattr(self, "__graphs__", {}))

class Edge(Model, metaclass=EDGE):
    __is_base_model__ = True

    @property
    def __order__(self):
        return len(getattr(self, "__nodes__", set()))

    def orderof(self):
        return self.__order__

    def nodesof(self):
        return set(getattr(self, "__nodes__", set()))

    def graphsof(self):
        return set(getattr(self, "__graphs__", []))

    def __issub__(self, other):
        if not hasattr(other, "__nodes__"):
            return False
        nodes_self = set(getattr(self, "__nodes__", set()))
        nodes_other = set(getattr(other, "__nodes__", set()))
        return nodes_self.issubset(nodes_other)

    def __contains__(self, item):
        return item in getattr(
            self,
            "__nodes__",
            set()
        )

class Arrow(Model, metaclass=ARROW):
    __is_base_model__ = True

    @property
    def __order__(self):
        return len(getattr(self, "__nodes__", []))

    def orderof(self):
        return self.__order__

    def nodesof(self):
        return list(getattr(self, "__nodes__", []))

    def graphsof(self):
        return set(getattr(self, "__graphs__", []))

    def __issub__(self, other):
        if not hasattr(other, "__nodes__"):
            return False
        nodes_self = list(getattr(self, "__nodes__", []))
        nodes_other = list(getattr(other, "__nodes__", []))
        return nodes_self == nodes_other

    def __contains__(self, item):
        return item in getattr(
            self,
            "__nodes__",
            []
        )

Loop = Filtered(Union(Edge, Arrow), _is_loop)
prop.set.nameof(Loop, "Loop")

class Graph(metaclass=GRAPH):
    __is_base_graph__ = True

    @property
    def __order__(self):
        edges = getattr(self, "__edges__", set())
        if not edges:
            return 0
        return max(getattr(e, "__order__", 0) for e in edges)

    def __call__(self, *args, **kwargs):
        return self

    def __size__(self):
        return self.sizeof()

    def __issub__(self, other):
        from graph.helper.types import _issub
        return _issub(self, other, "__edges__")

    def __contains__(self, item):
        from graph.helper.types import _contains
        return _contains(self, item, "__edges__")

    @property
    def add(self):
        if not hasattr(self, "_add"):
            from graph.helper.types import _GraphAdd
            self._add = _GraphAdd(self)
        return self._add

    @property
    def rm(self):
        if not hasattr(self, "_rm"):
            from graph.helper.types import _GraphRm
            self._rm = _GraphRm(self)
        return self._rm

    def nodesof(self):
        return getattr(
            self,
            "__nodes__",
            set()
        )

    def edgesof(self):
        return getattr(self, "__edges__", set())

    def sizeof(self):
        from graph.mods.prop import prop
        return prop.sizeof(self)

    def loopsof(self):
        return

    def compof(self, item):
        from graph.mods.prop import prop
        return prop.compof(entity=self, item=item)

    def compsof(self):
        from graph.mods.prop import prop
        return prop.compsof(entity=self)

    def cleanup(self):
        active_nodes = set()
        for e in getattr(self, "__edges__", set()):
            active_nodes.update(getattr(e, "__nodes__", []))
        getattr(self, "__nodes__", set()).intersection_update(active_nodes)
        return self

class Digraph(Graph, metaclass=DIGRAPH):
    @property
    def __order__(self):
        arrows = getattr(self, "__arrows__", None)
        if arrows is None:
            arrows = getattr(self, "__edges__", set())
        if not arrows:
            return 0
        return max(getattr(a, "__order__", 0) for a in arrows)

    def __call__(self, *args, **kwargs):
        return self

    def __issub__(self, other):
        from graph.helper.types import _issub
        return _issub(self, other, "__arrows__")

    def __contains__(self, item):
        from graph.helper.types import _contains
        return _contains(self, item, "__edges__")

    @property
    def add(self):
        if not hasattr(self, "_add"):
            from graph.helper.types import _DigraphAdd
            self._add = _DigraphAdd(self)
        return self._add

    @property
    def rm(self):
        if not hasattr(self, "_rm"):
            from graph.helper.types import _DigraphRm
            self._rm = _DigraphRm(self)
        return self._rm

    def arrowsof(self):
        return getattr(
            self,
            "__edges__",
            set()
        )
