import weakref
from typed.meta import TYPE
from typed.func import closure
from model.helper.meta import _resolve

@closure(lt="__issub__")
class MODEL(TYPE):
    __cache__ = weakref.WeakValueDictionary()

    def __isterm__(typ, trm):
        from typed.mods.typesystem import isterm

        if getattr(typ, '__is_base_model__', False):
            return (isinstance(trm, type) and issubclass(trm, typ)) or isinstance(trm, typ)

        if isinstance(trm, typ):
            return True

        fields = getattr(typ, "__fields__", {})
        for key, expected_type in fields.items():
            if not hasattr(trm, key):
                return False
            if not isterm(getattr(trm, key), expected_type):
                return False
        return True

    def __issub__(typ, other):
        from model.helper.meta import _schema
        from model.mods.check import check

        if isinstance(typ, MODEL) and isinstance(other, MODEL):
            return check.issub(_schema(typ), _schema(other))

        return False

    def __join__(typ, other):
        from model.mods.check import check
        if check.model.ismodel(other):
            base_model = next((b for b in typ.__mro__ if getattr(b, '__is_base_model__', False)), typ)
            return base_model(__extends__=[typ, other])
        return NotImplemented

    def __coprod__(typ, *args, **kwargs):
        components = {typ.__name__: typ}

        for arg in args:
            if isinstance(arg, type):
                components[arg.__name__] = arg

        for k, v in kwargs.items():
            if isinstance(v, type):
                components[k] = v
                if v.__name__ in components and components[v.__name__] is v and k != v.__name__:
                    components.pop(v.__name__)
            elif isinstance(v, str):
                old_name = k.__name__ if isinstance(k, type) else k
                if old_name in components:
                    cls = components.pop(old_name)
                    components[v] = cls

        base_model = next((b for b in typ.__mro__ if getattr(b, '__is_base_model__', False)), typ)
        return base_model(**components)

    def __call__(met, __origin_cls__=None, __defaults__=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            from model.mods.check import require
            require.model.validate(met, fields)

            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        bases, _fields, _defaults = _resolve(
            met, fields, __origin_cls__=__origin_cls__, __extends__=__extends__, __defaults__=__defaults__
        )

        cache_key = (met, frozenset(_fields.items()), __origin_cls__, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"Model({', '.join(f'{k}={nameof(v)}' for k, v in _fields.items())})" if _fields else "Model"

        _display_name = display_name

        class Model(*bases, metaclass=MODEL):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(Model, k, v)

        Model.__name__ = getattr(__origin_cls__, '__name__', display_name) if __origin_cls__ else display_name
        met.__cache__[cache_key] = Model
        return Model


class ORDERED_MODEL(MODEL):
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False
        fields = getattr(typ, "__fields__", None)
        if fields is not None:
            trm_fields = getattr(trm, "__fields__", {})
            filtered_term_keys = [k for k in trm_fields if k in fields]
            if filtered_term_keys != list(fields.keys()):
                return False
        return True

    def __issub__(typ, other):
        if not isinstance(typ, ORDERED_MODEL) or not isinstance(other, ORDERED_MODEL):
            return False

        return super(ORDERED_MODEL, typ).__issub__(other)

    def __call__(met, __origin_cls__=None, __defaults__=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            from model.mods.check import require
            require.model.validate(met, fields)

            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        bases, _fields, _defaults = _resolve(
            met, fields, __origin_cls__=__origin_cls__, __extends__=__extends__, __defaults__=__defaults__
        )

        cache_key = (met, tuple(_fields.items()), __origin_cls__, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"OrderedModel({', '.join(f'{k}={nameof(v)}' for k, v in _fields.items())})" if _fields else "OrderedModel"

        _display_name = display_name

        class OrderedModel(*bases, metaclass=ORDERED_MODEL):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(OrderedModel, k, v)

        OrderedModel.__name__ = getattr(__origin_cls__, '__name__', display_name) if __origin_cls__ else display_name
        met.__cache__[cache_key] = OrderedModel
        return OrderedModel


class STRICT_MODEL(MODEL):
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False
        fields = getattr(typ, "__fields__", None)
        if fields is not None:
            trm_fields = getattr(trm, "__fields__", {})
            if len(trm_fields) != len(fields):
                return False
        return True

    def __issub__(typ, other):
        if not isinstance(typ, STRICT_MODEL) or not isinstance(other, STRICT_MODEL):
            return False

        return super(STRICT_MODEL, typ).__issub__(other)

    def __call__(met, __origin_cls__=None, __defaults__=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            from model.mods.check import require
            require.model.validate(met, fields)

            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        bases, _fields, _defaults = _resolve(
            met, fields, __origin_cls__=__origin_cls__, __extends__=__extends__, __defaults__=__defaults__
        )

        cache_key = (met, frozenset(_fields.items()), __origin_cls__, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"StrictModel({', '.join(f'{k}={nameof(v)}' for k, v in _fields.items())})" if _fields else "StrictModel"

        _display_name = display_name

        class StrictModel(*bases, metaclass=STRICT_MODEL):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(StrictModel, k, v)

        StrictModel.__name__ = getattr(__origin_cls__, '__name__', display_name) if __origin_cls__ else display_name
        met.__cache__[cache_key] = StrictModel
        return StrictModel

class LAZY_MODEL(MODEL):
    def __call__(met, __origin_cls__=None, __defaults__=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        bases, _fields, _defaults = _resolve(
            met, fields, __origin_cls__=__origin_cls__, __extends__=__extends__, __defaults__=__defaults__
        )

        cache_key = (met, frozenset(_fields.items()), __origin_cls__, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"LazyModel({', '.join(f'{k}={nameof(v)}' for k, v in _fields.items())})" if _fields else "LazyModel"

        _display_name = display_name

        class LazyModel(*bases, metaclass=LAZY_MODEL):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(LazyModel, k, v)

        LazyModel.__name__ = getattr(__origin_cls__, '__name__', display_name) if __origin_cls__ else display_name
        met.__cache__[cache_key] = LazyModel
        return LazyModel


class LAZY_ORDERED_MODEL(LAZY_MODEL, ORDERED_MODEL):
    def __call__(met, __origin_cls__=None, __defaults__=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        bases, _fields, _defaults = _resolve(
            met, fields, __origin_cls__=__origin_cls__, __extends__=__extends__, __defaults__=__defaults__
        )

        cache_key = (met, tuple(_fields.items()), __origin_cls__, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"LazyOrderedModel({', '.join(f'{k}={nameof(v)}' for k, v in _fields.items())})" if _fields else "LazyOrderedModel"

        _display_name = display_name

        class LazyOrderedModel(*bases, metaclass=LAZY_ORDERED_MODEL):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(LazyOrderedModel, k, v)

        LazyOrderedModel.__name__ = getattr(__origin_cls__, '__name__', display_name) if __origin_cls__ else display_name
        met.__cache__[cache_key] = LazyOrderedModel
        return LazyOrderedModel


class LAZY_STRICT_MODEL(LAZY_MODEL, STRICT_MODEL):
    def __call__(met, __origin_cls__=None, __defaults__=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_model__', False):
            instance = super().__call__()
            for k, v in fields.items():
                setattr(instance, k, v)
            return instance

        bases, _fields, _defaults = _resolve(
            met, fields, __origin_cls__=__origin_cls__, __extends__=__extends__, __defaults__=__defaults__
        )

        cache_key = (met, frozenset(_fields.items()), __origin_cls__, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        from typed.mods.typesystem import nameof
        display_name = f"LazyStrictModel({', '.join(f'{k}={nameof(v)}' for k, v in _fields.items())})" if _fields else "LazyStrictModel"

        _display_name = display_name

        class LazyStrictModel(*bases, metaclass=LAZY_STRICT_MODEL):
            __kind__ = "type"
            __display__ = _display_name
            __fields__ = _fields
            __defaults__ = _defaults
            __is_base_model__ = False

        for k, v in fields.items():
            type.__setattr__(LazyStrictModel, k, v)

        LazyStrictModel.__name__ = getattr(__origin_cls__, '__name__', display_name) if __origin_cls__ else display_name
        met.__cache__[cache_key] = LazyStrictModel
        return LazyStrictModel
