class _SchemaDescriptor:
    def __get__(self, instance, owner):
        from model.mods.func import schema as _schema
        target = owner if instance is None else instance

        def schema():
            return _schema(target)

        schema.__name__ = "schema"
        return schema

class _ReduceDescriptor:
    def __get__(self, instance, owner):
        from model.mods.func import reduce as _reduce
        target = owner if instance is None else instance

        def reduce(**kwargs):
            return _reduce(target, **kwargs)

        reduce.__name__ = "reduce"
        return reduce
