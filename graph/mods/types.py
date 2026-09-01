from graph.mods.meta import NODE, EDGE, GRAPH, DIGRAPH, ACYCLIC
from model import Model
from graph.helper.types import _GraphAdd, _GraphRm, _AcyclicAdd, _DigraphAdd

class Node(Model, metaclass=NODE):
    __is_base_model__ = True

    def graphsof(self):
        return set(getattr(self, "__graphs__", []))

class Edge(Model, metaclass=EDGE):
    __is_base_model__ = True

    def orderof(self):
        return getattr(self, "__order__", -1)

    def nodesof(self):
        return set(getattr(self, "__nodes__", []))

    def graphsof(self):
        return set(getattr(self, "__graphs__", []))

    def __issub__(self, other):
        if not hasattr(other, "__nodes__"):
            return False
        nodes_self = set(getattr(self, "__nodes__", []))
        nodes_other = set(getattr(other, "__nodes__", []))
        return nodes_self.issubset(nodes_other)

    def __contains__(self, item):
        return item in getattr(self, "__nodes__", [])

class Graph(metaclass=GRAPH):
    __is_base_graph__ = True

    def __call__(self, *args, **kwargs) -> 'Graph':
        return self

    def __size__(self):
        return self.sizeof()

    def __issub__(self, other):
        if not hasattr(other, "__nodes__") or not hasattr(other, "__edges__"):
            return False
        sub_nodes = getattr(self, "__nodes__", set())
        sup_nodes = getattr(other, "__nodes__", set())
        if not sub_nodes.issubset(sup_nodes):
            return False
        sub_edges = getattr(self, "__edges__", set())
        sup_edges = getattr(other, "__edges__", set())
        return sub_edges.issubset(sup_edges)

    def __contains__(self, item):
        if item in getattr(self, "__nodes__", set()):
            return True
        return item in getattr(self, "__edges__", set())

    @property
    def add(self) -> _GraphAdd:
        if not hasattr(self, "_add"):
            self._add = _GraphAdd(self)
        return self._add

    @property
    def rm(self) -> _GraphRm:
        if not hasattr(self, "_rm"):
            self._rm = _GraphRm(self)
        return self._rm

    def nodesof(self):
        return getattr(self, "__nodes__", set())

    def edgesof(self):
        return getattr(self, "__edges__", set())

    def orderof(self):
        return len(getattr(self, "__nodes__", set()))

    def sizeof(self):
        return len(getattr(self, "__nodes__", set())) + len(getattr(self, "__edges__", set()))

    def loopsof(self):
        return {e for e in getattr(self, "__edges__", set()) if len(set(getattr(e, "__nodes__", []))) == 1}

    def cleanup(self):
        active_nodes = set()
        for e in getattr(self, "__edges__", set()):
            active_nodes.update(getattr(e, "__nodes__", []))
        getattr(self, "__nodes__", set()).intersection_update(active_nodes)
        return self

class Acyclic(Graph, metaclass=ACYCLIC):
    def __call__(self, *args, **kwargs) -> 'Acyclic':
        return self

    @property
    def add(self) -> _AcyclicAdd:
        if not hasattr(self, "_add"):
            self._add = _AcyclicAdd(self)
        return self._add

class Digraph(Graph, metaclass=DIGRAPH):
    def __call__(self, *args, **kwargs) -> 'Digraph':
        return self

    @property
    def add(self) -> _DigraphAdd:
        if not hasattr(self, "_add"):
            self._add = _DigraphAdd(self)
        return self._add
