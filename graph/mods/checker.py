from typed.checker import Checker
from typed.mods.typesystem import iscongruent

class GraphChecker(Checker):
    def isnode(self, entity) -> bool:
        from graph.mods.types import Node
        if self.explode:
            from typed import require
            require.isterm(entity, Node)

        from typed import check
        return check.isterm(entity, Node)

    def isedge(self, entity) -> bool:
        from graph.mods.types import Edge

        if self.explode:
            from typed import require
            require.isterm(entity, Edge)

        from typed import check
        return check.isterm(entity, Edge)

    def isdirected(self, entity) -> bool:
        is_dir = getattr(entity, "__directed__", False) is True

        if not is_dir and self.explode:
            from typed.err import TypeErr
            raise TypeErr(
                message="Entity is not directed",
                term=entity
            )

        return is_dir

    def isarrow(self, entity) -> bool:
        if not self.isedge(entity) or not self.isdirected(entity):
            return False

        return True

    def ishyper(self, entity) -> bool:
        order = getattr(entity, "__order__", None)

        if order is None:
            nodes = getattr(entity, "__nodes__", None)
            if nodes is not None:
                order = len(nodes)

        is_hyper = order != 2

        if not is_hyper and self.explode:
            from typed.err import TypeErr
            raise TypeErr(
                message="Entity is not hyper (order is 2)",
                term=entity
            )

        return is_hyper

    def isloop(self, entity) -> bool:
        from graph.mods.prop import prop
        from typed import NotDefined
        nodes = prop.nodesof(entity)
        if nodes is NotDefined:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    message="Entity has no nodes",
                    term=entity
                )
            return False

        is_l = len(set(nodes)) == 1

        if not is_l and self.explode:
            from typed.err import TypeErr
            raise TypeErr(
                message="Edge is not a loop",
                term=entity
            )
        return is_l

    def isorphan(self, node, graph=None) -> bool:
        if not self.isnode(node):
            if self.explode:
                from typed.err import TypeErr
                raise TypeErr(
                    message="Entity is not a node",
                    term=node,
                    expected=("Node",)
                )
            return False

        from graph.mods.prop import prop
        from typed import NotDefined

        graphs = getattr(node, "__graphs__", set())

        if graph is not None:
            if graph not in graphs:
                if self.explode:
                    from typed.err import TypeErr
                    raise TypeErr(
                        message="Node does not belong to the specified graph",
                        term=node,
                        expected=("Node in specified graph",)
                    )
                return False

            try:
                degree = prop.degreeof(graph, node)
            except Exception:
                if self.explode:
                    raise
                return False

            if degree is NotDefined:
                if self.explode:
                    from typed.err import TypeErr
                    raise TypeErr(
                        message="Node not found in graph or invalid graph structure",
                        term=node,
                        expected=("Node in graph",)
                    )
                return False

            is_orph = degree == 0
            if not is_orph and self.explode:
                from typed.err import TypeErr
                raise TypeErr(
                    message="Node is not an orphan (degree > 0) in the specified graph",
                    term=node,
                    expected=("Orphan node",)
                )
            return is_orph

        if not graphs:
            return True

        for g in graphs:
            try:
                degree = prop.degreeof(g, node)
            except Exception:
                if self.explode:
                    raise
                return False

            if degree is not NotDefined and degree > 0:
                if self.explode:
                    from typed.err import TypeErr
                    raise TypeErr(
                        message="Node is not an orphan in at least one of its graphs",
                        term=node,
                        expected=("Orphan node in all graphs",)
                    )
                return False
        return True

    def isgraph(self, entity) -> bool:
        from graph.mods.types import Graph

        if self.explode:
            from typed import require
            require.isterm(entity, Graph)

        from typed import check
        return check.isterm(entity, Graph)

    def isacyclic(self, entity) -> bool:
        from graph.mods.types import Acyclic

        if self.explode:
            from typed import require
            require.isterm(entity, Acyclic)

        from typed import check
        return check.isterm(entity, Acyclic)

    def isregular(self, entity) -> bool:
        from graph.mods.prop import prop
        from typed import NotDefined

        nodes = prop.nodesof(entity)
        edges = prop.edgesof(entity)

        if nodes is NotDefined or edges is NotDefined:
            if self.explode:
                from typed import TypeErr
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
            from typed.err import TypeErr
            raise TypeErr(
                message="Graph is not regular",
                term=entity
            )
        return is_reg

    def iscomplete(self, entity) -> bool:
        from graph.mods.prop import prop
        from typed import NotDefined

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
            from typed.err import TypeErr
            raise TypeErr(
                message="Graph is not complete",
                term=entity
            )
        return is_comp

    def isconnected(
        self,
        entity
    ) -> bool:
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
        comps = list(prop.componentsof(entity))
        is_conn = len(comps) == 1
        if not is_conn and self.explode:
            raise TypeErr(
                message="Graph is not connected",
                term=entity
            )
        return is_conn

__require__ = GraphChecker(
    quantifier=None,
    explode=True
)

__check__ = GraphChecker(
    quantifier=None,
    explode=False
)

class check:
    some   = __check__.some
    every  = __check__.every
    none   = __check__.none
    only   = __check__.only

    class node:
        isnode = __check__.isnode
        isorphan = __check__.isorphan

    class edge:
        isedge = __check__.isedge
        isloop = __check__.isloop
        isarrow = __check__.isarrow
        ishyper = __check__.ishyper

    class graph:
        isgraph     = __check__.isgraph
        isdirected  = __check__.isdirected
        isregular   = __check__.isregular
        isacyclic   = __check__.isacyclic
        iscomplete  = __check__.iscomplete
        isconnected = __check__.isconnected

class require:
    some   = __require__.some
    every  = __require__.every
    none   = __require__.none
    only   = __require__.only

    class node:
        isnode = __require__.isnode
        isorphan = __require__.isorphan

    class edge:
        isedge = __require__.isedge
        isloop = __require__.isloop
        isarrow = __require__.isarrow
        ishyper = __require__.ishyper

    class graph:
        isgraph     = __require__.isgraph
        isdirected  = __require__.isdirected
        isregular   = __require__.isregular
        isacyclic   = __require__.isacyclic
        iscomplete  = __require__.iscomplete
        isconnected = __require__.isconnected
