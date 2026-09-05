from typed.checker import Checker

class BaseChecker(Checker):
    def isnode(self, entity):
        from typed.checker import typecheck
        from graph.mods.types import Node
        return typecheck(self, entity, Node)

    def isedge(self, entity):
        from typed.checker import typecheck
        from graph.mods.types import Edge
        return typecheck(self, entity, Edge)

    def isarrow(self, entity):
        from typed.checker import typecheck
        from graph.mods.types import Arrow
        return typecheck(self, entity, Arrow)

    def isgraph(self, entity):
        from typed.checker import typecheck
        from graph.mods.types import Graph
        return typecheck(self, entity, Graph)

    def isdigraph(self, entity):
        from typed.checker import typecheck
        from graph.mods.types import Digraph
        return typecheck(self, entity, Digraph)

class NodeChecker(Checker):
    def isorphan(self, node, graph=None):
        if not self.isnode(node):
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    message="Entity is not a node",
                    term=node,
                    expected=("Node",)
                )
            return False

        from graph.mods.prop import prop
        from typed.mods.err import NotDefined

        if graph is not None:
            try:
                degree = prop.degreeof(graph, node)
            except Exception:
                if self.explode:
                    raise
                return False

            is_orph = degree == 0
            if not is_orph and self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    message="Node is not an orphan in the specified graph",
                    term=node,
                    expected=("Orphan node",)
                )
            return is_orph

        graphs = getattr(node, "__graphs__", None)
        if not graphs:
            return True

        for g in graphs:
            try:
                degree = prop.degreeof(g, node)
            except Exception:
                if self.explode:
                    raise
                return False

            if degree is NotDefined or degree > 0:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        message="Node is not an orphan in at least one of its graphs",
                        term=node,
                        expected=("Orphan node in all graphs",)
                    )
                return False

        return True

class GeneralChecker(Checker):
    def ishyper(self, entity):
        order = getattr(entity, "__order__", None)
        return True if isinstance(order, int) and order > 2 else False

class LineChecker(GeneralChecker):
    def isloop(self, entity):
        from typed.checker import typecheck
        from graph.mods.types import Loop
        return typecheck(self, entity, Loop)

class GraphChecker(BaseChecker):
    def isacyclic(self, entity):
        from graph.mods.types import Acyclic
        if self.explode:
            from typed.mods.check import require
            require.isterm(entity, Acyclic)
        from typed.mods.check import check
        return check.isterm(entity, Acyclic)

    def isregular(self, entity):
        from graph.mods.prop import prop
        from typed.mods.err import NotDefined
        nodes = prop.nodesof(entity)
        edges = prop.edgesof(entity)
        if nodes is NotDefined or edges is NotDefined:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    message="Entity is missing nodes or edges",
                    term=entity
                )
            return False
        if not nodes:
            return True
        degrees = {n: 0 for n in nodes}
        for e in edges:
            for n in getattr(e, "__nodes__", []):
                if n in degrees:
                    degrees[n] += 1
        is_reg = len(set(degrees.values())) <= 1
        if not is_reg and self.explode:
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="Graph is not regular",
                term=entity
            )
        return is_reg

    def iscomplete(self, entity):
        from graph.mods.prop import prop
        from typed.mods.err import NotDefined
        nodes = prop.nodesof(entity)
        edges = prop.edgesof(entity)
        if nodes is NotDefined or edges is NotDefined:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    message="Entity is missing nodes or edges",
                    term=entity
                )
            return False
        nodes_set = set(nodes)
        is_comp = all(set(getattr(e, "__nodes__", [])) == nodes_set for e in edges)
        if not is_comp and self.explode:
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="Graph is not complete",
                term=entity
            )
        return is_comp

    def isconnected(self, entity):
        from graph.mods.prop import prop
        from typed.mods.err import NotDefined
        from typed.mods.err import TypeErr
        nodes = prop.nodesof(entity)
        if nodes is NotDefined:
            if self.explode:
                raise TypeErr(
                    message="Entity is missing nodes or edges",
                    term=entity
                )
            return False
        if not nodes:
            return True
        comps = list(prop.compsof(entity))
        is_conn = len(comps) == 1
        if not is_conn and self.explode:
            raise TypeErr(
                message="Graph is not connected",
                term=entity
            )
        return is_conn

class DigraphChecker(BaseChecker):
    def isdag(self, entity):
        if self.explode:
            __digraph_require__.isdigraph(entity)
            __graph_require__.isacyclic(entity)
            return True
        return self.isdigraph(entity) and __graph_check__.isacyclic(entity)

__graph_require__ = GraphChecker(quantifier=None, explode=True)
__graph_check__ = GraphChecker(quantifier=None, explode=False)
__digraph_require__ = DigraphChecker(quantifier=None, explode=True)
__digraph_check__ = DigraphChecker(quantifier=None, explode=False)

class check:
    class node:
        isnode = __graph_check__.isnode
        isorphan = __graph_check__.isorphan

    class edge:
        isedge = __graph_check__.isedge
        isloop = __graph_check__.isloop
        ishyper = __graph_check__.ishyper

    class arrow:
        isarrow = __digraph_check__.isarrow
        isloop = __digraph_check__.isloop
        ishyper = __digraph_check__.ishyper

    class graph:
        isgraph     = __graph_check__.isgraph
        isregular   = __graph_check__.isregular
        isacyclic   = __graph_check__.isacyclic
        iscomplete  = __graph_check__.iscomplete
        isconnected = __graph_check__.isconnected

    class digraph:
        isdigraph   = __digraph_check__.isdigraph
        isdag       = __digraph_check__.isdag

class require:
    class node:
        isnode = __graph_require__.isnode
        isorphan = __graph_require__.isorphan

    class edge:
        isedge = __graph_require__.isedge
        isloop = __graph_require__.isloop
        ishyper = __graph_require__.ishyper

    class arrow:
        isarrow = __digraph_require__.isarrow
        isloop = __digraph_require__.isloop
        ishyper = __digraph_require__.ishyper

    class graph:
        isgraph     = __graph_require__.isgraph
        isregular   = __graph_require__.isregular
        isacyclic   = __graph_require__.isacyclic
        iscomplete  = __graph_require__.iscomplete
        isconnected = __graph_require__.isconnected

    class digraph:
        isdigraph   = __digraph_require__.isdigraph
        isdag       = __digraph_require__.isdag
