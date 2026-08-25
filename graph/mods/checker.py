from typed.mods.check import Checker

class GraphChecker(Checker):
    def isnode(self, entity) -> bool:
        from graph.mods.types import Node
        if self.explode:
            from typed.mods.check import require
            require.isterm(entity, Node)

        from typed.mods.check import check
        return check.isterm(entity, Node)

    def isedge(self, entity) -> bool:
        from graph.mods.types import Edge

        if self.explode:
            from typed.mods.check import require
            require.isterm(entity, Edge)

        from typed.mods.check import check
        return check.isterm(entity, Edge)

    def isarrow(self, entity) -> bool:
        if not self.isedge(entity):
            return False

        is_dir = getattr(entity, "__directed__", False) is True

        if not is_dir and self.explode:
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="Edge is not directed (not an arrow)",
                term=entity
            )

        return is_dir

    def isdirected(self, entity) -> bool:
        is_dir = getattr(entity, "__directed__", False) is True

        if not is_dir and self.explode:
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="Entity is not directed",
                term=entity
            )

        return is_dir

    def ishyper(self, entity) -> bool:
        order = getattr(entity, "__order__", None)

        if order is None:
            nodes = getattr(entity, "__nodes__", None)
            if nodes is not None:
                order = len(nodes)

        is_hyper = order != 2

        if not is_hyper and self.explode:
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="Entity is not hyper (order is 2)",
                term=entity
            )

        return is_hyper

    def isloop(self, entity) -> bool:
        from graph.mods.prop import prop
        from typed.mods.err import NotDefined
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
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="Edge is not a loop",
                term=entity
            )
        return is_l

    def isgraph(self, entity) -> bool:
        from graph.mods.types import Graph

        if self.explode:
            from typed.mods.check import require
            require.isterm(entity, Graph)

        from typed.mods.check import check
        return check.isterm(entity, Graph)

    def isacyclic(self, entity) -> bool:
        from graph.mods.types import Acyclic

        if self.explode:
            from typed.mods.check import require
            require.isterm(entity, Acyclic)

        from typed.mods.check import check
        return check.isterm(entity, Acyclic)

    def isregular(self, entity) -> bool:
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

    def iscomplete(self, entity) -> bool:
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

require = GraphChecker(
    quantifier=None,
    explode=True
)

check = GraphChecker(
    quantifier=None,
    explode=False
)
