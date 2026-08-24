def node(__cls__=None, *, check=None, lazy=None, strict=None, ordered=None):
    def decorator(c):
        from model.resolve import resolve
        from typed.func import hints
        from graph.mods.types import Node

        lz = resolve.model.lazy(lazy)
        chk = resolve.model.check(check)
        st = resolve.model.strict(strict)
        od = resolve.model.ordered(ordered)

        try:
            fields = hints(c)
        except Exception:
            fields = {}

        defaults = {k: getattr(c, k) for k in fields if hasattr(c, k)}
        extends = [b for b in c.__bases__ if b is not object]

        cls_node = Node(
            __origin_cls__=c,
            __defaults__=defaults,
            __extends__=extends,
            **fields
        )

        cls_node.__lazy__ = lz
        cls_node.__check__ = chk
        cls_node.__strict__ = st
        cls_node.__ordered__ = od

        return cls_node

    if __cls__ is None:
        return decorator
    return decorator(__cls__)


def edge(__cls__=None, *, check=None, lazy=None, strict=None, ordered=None, directed=None, nodes=None, order=None):
    def decorator(c):
        from model.resolve import resolve
        from typed.func import hints
        from graph.mods.types import Edge

        lz = resolve.model.lazy(lazy)
        chk = resolve.model.check(check)
        st = resolve.model.strict(strict)
        od = resolve.model.ordered(ordered)

        try:
            fields = hints(c)
        except Exception:
            fields = {}

        defaults = {k: getattr(c, k) for k in fields if hasattr(c, k)}
        extends = [b for b in c.__bases__ if b is not object]

        cls_edge = Edge(
            *(nodes if nodes is not None else []),
            __origin_cls__=c,
            __defaults__=defaults,
            __extends__=extends,
            **fields
        )

        cls_edge.__lazy__ = lz
        cls_edge.__check__ = chk
        cls_edge.__strict__ = st
        cls_edge.__ordered__ = od

        if directed is not None:
            cls_edge.__directed__ = directed
        if order is not None:
            cls_edge.__order__ = order

        return cls_edge

    if __cls__ is None:
        return decorator
    return decorator(__cls__)
