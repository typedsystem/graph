from typed.resolve import resolve as typed_resolve, resolved, resolver

class resolve(typed_resolve):
    class model:
        @resolver
        def check(__check__=None, conf=None):
            from typed.mods.err import NotDefined
            if __check__ is not None and __check__ is not NotDefined:
                return __check__

            if conf is None:
                try:
                    from model.mods.init import conf
                except ImportError:
                    pass

            default_val = getattr(conf.model, 'check', True) if conf and hasattr(conf, 'model') else True
            return resolved(provided=__check__, default=default_val)

        @resolver
        def lazy(lazy=None, conf=None):
            from typed.mods.err import NotDefined
            if lazy is not None and lazy is not NotDefined:
                return lazy

            if conf is None:
                try:
                    from model.mods.init import conf
                except ImportError:
                    pass

            default_val = getattr(conf.model, 'lazy', False) if conf and hasattr(conf, 'model') else False
            return resolved(provided=lazy, default=default_val)

        @resolver
        def strict(strict=None, conf=None):
            from typed.mods.err import NotDefined
            if strict is not None and strict is not NotDefined:
                return strict

            if conf is None:
                try:
                    from model.mods.init import conf
                except ImportError:
                    pass

            default_val = getattr(conf.model, 'strict', False) if conf and hasattr(conf, 'model') else False
            return resolved(provided=strict, default=default_val)

        @resolver
        def ordered(ordered=None, conf=None):
            from typed.mods.err import NotDefined
            if ordered is not None and ordered is not NotDefined:
                return ordered

            if conf is None:
                try:
                    from model.mods.init import conf
                except ImportError:
                    pass

            default_val = getattr(conf.model, 'ordered', False) if conf and hasattr(conf, 'model') else False
            return resolved(provided=ordered, default=default_val)
