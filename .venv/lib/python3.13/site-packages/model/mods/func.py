from typing import TypeVar, Type, TYPE_CHECKING, Union, Any, Dict
from typed.poly import Poly

if TYPE_CHECKING:
    from model.mods.types.model import Model
    from model.mods.types.schema import Schema

T = TypeVar('T')

class model:
    def __new__(cls, __cls__: Type[T] = None, *, check: bool = None, lazy: bool = None, strict: bool = None, ordered: bool = None):

        def decorator(c: Type[T]) -> 'Union[Type[T], Type[Model]]':
            from model.mods.resolve import resolve
            from model.mods.types.model import (
                Model, OrderedModel, StrictModel,
                LazyModel, LazyOrderedModel, LazyStrictModel
            )

            lz = resolve.model.lazy(lazy)
            chk = resolve.model.check(check)
            st = resolve.model.strict(strict)
            od = resolve.model.ordered(ordered)

            try:
                from typed.mods.func import hints
                fields = hints(c)
            except Exception:
                fields = {}

            defaults = {k: getattr(c, k) for k in fields if hasattr(c, k)}
            extends = [b for b in c.__bases__ if b is not object]

            if lz:
                if od:
                    return LazyOrderedModel(__origin_cls__=c, __defaults__=defaults, __extends__=extends, **fields)
                if st:
                    return LazyStrictModel(__origin_cls__=c, __defaults__=defaults, __extends__=extends, **fields)
                return LazyModel(__origin_cls__=c, __defaults__=defaults, __extends__=extends, **fields)
            else:
                if od:
                    return OrderedModel(__origin_cls__=c, __defaults__=defaults, __extends__=extends, **fields)
                if st:
                    return StrictModel(__origin_cls__=c, __defaults__=defaults, __extends__=extends, **fields)
                return Model(__origin_cls__=c, __defaults__=defaults, __extends__=extends, **fields) 

        if __cls__ is None:
            return decorator
        return decorator(__cls__)

    @staticmethod
    def strict(__cls__: Type[T] = None, *, check: bool = None, lazy: bool = None) -> 'Union[Type[T], Type[Model]]':
        return model(__cls__, check=check, lazy=lazy, strict=True)

    @staticmethod
    def ordered(__cls__: Type[T] = None, *, check: bool = None, lazy: bool = None) -> 'Union[Type[T], Type[Model]]':
        return model(__cls__, check=check, lazy=lazy, ordered=True)

def field(func: callable) -> property:
    """
    The field decorator
    """
    from typed.func import hints
    from typed.err import NotDefined
    import functools

    h = hints(func)
    if 'return' not in h:
        from model.mods.err import FieldErr
        raise FieldErr(
            message=f"Dynamic field has no codomain",
            field=func,
            expected="some type",
            received=NotDefined
        )

    from typed.mods.func import signature
    sig = signature(func)

    @functools.wraps(func)
    def getter(self):
        value = func(self)
        from model.mods.check import check

        if not check.bind.cod(func, sig, value):
            from model.mods.err import FieldErr
            raise FieldErr(
                message=f"Field returned invalid type.",
                key=func,
                field=value,
                expected=(sig.cod,),
                received=type(value)
            )
        return value

    return property(getter)

def schema(obj: 'Union[Model, Type[Model], Any]') -> 'Type[Schema]':
    from model.mods.check import check

    if check.schema.isschema(obj):
        return obj

    if check.model.ismodel(obj):
        from model.mods.types.schema import Schema, OrderedSchema, StrictSchema
        from typed.func import hints
        from typed.prop import get
        from model.helper.func import _traverse

        raw_fields = dict(getattr(obj, "__fields__", {}))
        schema_fields = {}

        for k, v in raw_fields.items():
            schema_fields[k] = _traverse(v, callback=schema)
        for key in dir(obj):
            attr = getattr(obj, key, None)
            if isinstance(attr, property):
                h = hints(attr.fget)
                if 'return' in h:
                    schema_fields[key] = _traverse(h['return'], callback=schema)
        is_ordered = get(obj, "__flags__.model.is_ordered", False)

        if check.model.isstrict(obj):
            return StrictSchema(**schema_fields)
        if check.model.isordered(obj):
            return OrderedSchema(**schema_fields)
        return Schema(**schema_fields)

    from typed import prop
    meta = prop.typeof(obj)
    fields = getattr(meta, "__fields__", {})
    out = {}
    if fields:
        for key in fields:
            if hasattr(obj, key):
                out[key] = _traverse(getattr(obj, key), callback=schema)

    for key in dir(meta):
        attr = getattr(meta, key, None)
        if isinstance(attr, property):
            out[key] = _traverse(getattr(obj, key), callback=schema)

    return out

fields = Poly("__fields__")

def unwrap(obj: 'Union[Schema, Type[Schema], Any]') -> 'Dict[str, Any]':
    _fields = fields(obj)
    from typed.err import NotDefined

    if _fields is NotDefined:
        return obj

    if isinstance(obj, dict):
        return {k: unwrap(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [unwrap(v) for v in obj]

    if isinstance(obj, tuple):
        return tuple(unwrap(v) for v in obj)

    return {k: unwrap(v) for k, v in _fields.items()}

def reduce(typ, **kwargs):
    from model.mods.check import check

    if check.model.ismodel(typ):
        base_model = next((b for b in typ.__mro__ if getattr(b, '__is_base_model__', False)), typ)
        Reduced = base_model(__extends__=[typ], __defaults__=kwargs)

    elif check.schema.isschema(typ):
        base_schema = next((b for b in typ.__mro__ if getattr(b, '__is_base_schema__', False)), typ)
        Reduced = base_schema(__extends__=[typ])
    else:
        Reduced = typ

    for k, v in kwargs.items():
        setattr(Reduced, k, v)

    return Reduced
