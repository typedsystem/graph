from graph.mods.meta import NODE, EDGE, GRAPH

class Node(metaclass=NODE):
    __is_base_model__ = True

class Edge(metaclass=EDGE):
    __is_base_model__ = True

    def orderof(self):
        return getattr(self, "__order__", -1)

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

    @property
    def add(self):
        if not hasattr(self, "_add"):
            self._add = _GraphAdd(self)
        return self._add

    @property
    def rm(self):
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

    def degreeof(self, *nodes):
        nodes_set = set(nodes)
        graph_nodes = getattr(self, "__nodes__", set())
        if not nodes_set.issubset(graph_nodes):
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="One or more nodes not found in graph",
                term=nodes
            )
        count = 0
        for e in getattr(self, "__edges__", set()):
            if nodes_set.issubset(getattr(e, "__nodes__", [])):
                count += 1
        return count

    def cleanup(self):
        active_nodes = set()
        for e in getattr(self, "__edges__", set()):
            active_nodes.update(getattr(e, "__nodes__", []))
        getattr(self, "__nodes__", set()).intersection_update(active_nodes)
        return self

    def induced(self, *elements):
        explicit_nodes = set()
        explicit_edges = set()

        for el in elements:
            if hasattr(el, "__nodes__"):
                explicit_edges.add(el)
            else:
                explicit_nodes.add(el)

        nodes_set = set(explicit_nodes)
        for e in explicit_edges:
            nodes_set.update(getattr(e, "__nodes__", []))

        if not nodes_set.issubset(self.__nodes__):
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="One or more nodes not found in graph",
                term=elements
            )

        if not explicit_edges.issubset(self.__edges__):
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="One or more edges not found in graph",
                term=elements
            )

        subgraph = self.__class__()
        subgraph.__nodes__.update(nodes_set)

        for e in self.__edges__:
            if e in explicit_edges or set(getattr(e, "__nodes__", [])).issubset(explicit_nodes):
                subgraph.__edges__.add(e)

        return subgraph

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

Digraph = Graph(directed=True)
