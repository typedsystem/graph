from typed.mods.check import Checker

class GraphChecker(Checker):
    def isgraph(self, entity) -> bool:
        from graph.mods.types import Graph

        if self.explode:
            from typed.mods.check import require
            require.isterm(entity, Graph)

        from typed.mods.check import check
        return check.isterm(entity, Graph)

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

require = GraphChecker(
    quantifier=None,
    explode=True
)

check = GraphChecker(
    quantifier=None,
    explode=False
)
