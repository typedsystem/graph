from typed.func import closure
from typed.meta import DICT
from model.helper.meta import _resolve, _issub

@closure(lt="__issub__")
class SCHEMA(DICT):
    __cache__ = {}

    def __isterm__(typ, trm):
        from typed import prop
        if prop.get(typ, '__is_base_schema__', False):
            return isinstance(trm, type) and issubclass(trm, typ)

        from typed import every, check
        if not check.isinstance(trm, dict) and not check.issub(prop.typeof(trm, level=2), DICT):
            return False
        fields = prop.get(typ, "__fields__", None)
        if fields is not None:
            if not every(k in trm for k in fields):
                return False
            return every(check.isterm(trm[k], expected_type) for k, expected_type in fields.items())
        return False

    def __issub__(typ, other):
        if not isinstance(typ, SCHEMA) or not isinstance(other, SCHEMA):
            return False

        return _issub(typ.unwrap(), other.unwrap())

    def __join__(typ, other):
        from model.mods.check import check
        if check.schema.isschema(other):
            base_schema = next((b for b in typ.__mro__ if getattr(b, '__is_base_schema__', False)), typ)
            return base_schema(__extends__=[typ, other])
        return NotImplemented

    def __call__(met, typesystem=None, __check__: bool=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_schema__', False):
            from model.mods.check import require
            require.model.validate(met, fields)
            return dict(**fields)

        from model.mods.resolve import resolve
        from model.mods.check import require

        typesystem = resolve.typesystem.entity(typesystem)
        resolved_check = resolve.model.check(__check__)

        bases, _fields, _ = _resolve(met, fields, __extends__=__extends__)

        cache_key = (met, frozenset(_fields.items()), id(typesystem), resolved_check, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        if resolved_check and fields:
            require.every.ismember(set(fields.values()), typesystem)

        display_name = f"Schema({', '.join(f'{k}={typesystem.nameof(v)}' for k, v in _fields.items())})" if _fields else "Schema"

        from model.mods.flags import Flags, ModelFlags
        from typed.mods.init import TYPESYSTEM
        types_set = set(_fields.values()) if _fields else set()
        from typed import Str

        _types_set = types_set
        _display_name = display_name
        _resolved_check = resolved_check
        _typesystems = {TYPESYSTEM, typesystem}

        class Schema(*bases, metaclass=SCHEMA):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True, model=ModelFlags(is_schema=True))
            __typesystems__ = _typesystems
            __display__ = _display_name
            __fields__ = _fields
            __types__ = _types_set
            __key_type__ = Str
            __check__ = _resolved_check
            __is_base_schema__ = False

        for k, v in fields.items():
            type.__setattr__(Schema, k, v)

        Schema.__name__ = display_name
        met.__cache__[cache_key] = Schema
        return Schema


class ORDERED_SCHEMA(SCHEMA):
    def __isterm__(typ, trm):
        if getattr(typ, '__is_base_schema__', False):
            return isinstance(trm, type) and issubclass(trm, typ)
        if not super().__isterm__(trm):
            return False

        fields = getattr(typ, "__fields__", None)
        if fields is not None:
            filtered_term_keys = [k for k in trm if k in fields]
            if filtered_term_keys != list(fields.keys()):
                return False
        return True

    def __issub__(typ, other):
        from typed import prop
        from model.mods.check import check

        if not check.every.issub(
            (prop.typeof(typ), prop.typeof(other)),
            ORDERED_SCHEMA
        ):
            return False

        return super(ORDERED_SCHEMA, typ).__issub__(other)

    def __call__(met, typesystem=None, __check__: bool = None, __extends__=None, **fields):
        if not getattr(met, '__is_base_schema__', False):
            from model.mods.check import require
            require.model.validate(met, fields)
            return dict(**fields)

        from model.mods.resolve import resolve
        from model.mods.check import check
        from typed import Str

        typesystem = resolve.typesystem.entity(typesystem)
        resolved_check = resolve.model.check(__check__)

        bases, _fields, _ = _resolve(met, fields, __extends__=__extends__)

        cache_key = (met, tuple(_fields.items()), id(typesystem), resolved_check, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        if resolved_check and fields:
            check.every.ismember(set(fields.values()), typesystem)

        display_name = f"OrderedSchema({', '.join(f'{k}={typesystem.nameof(v)}' for k, v in _fields.items())})" if _fields else "OrderedSchema"

        from model.mods.flags import Flags, ModelFlags
        from typed.mods.init import TYPESYSTEM
        types_set = set(_fields.values()) if _fields else set()

        _display_name = display_name
        _resolved_check = resolved_check
        _typesystems = {TYPESYSTEM, typesystem}

        class OrderedSchema(*bases, metaclass=ORDERED_SCHEMA):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True, model=ModelFlags(is_schema=True, is_ordered=True))
            __typesystems__ = _typesystems
            __display__ = _display_name
            __fields__ = _fields
            __types__ = types_set
            __key_type__ = Str
            __check__ = _resolved_check
            __is_base_schema__ = False

        for k, v in fields.items():
            type.__setattr__(OrderedSchema, k, v)

        OrderedSchema.__name__ = display_name
        met.__cache__[cache_key] = OrderedSchema
        return OrderedSchema


class STRICT_SCHEMA(SCHEMA):
    def __isterm__(typ, trm):
        if getattr(typ, '__is_base_schema__', False):
            return isinstance(trm, type) and issubclass(trm, typ)
        if not super().__isterm__(trm):
            return False

        fields = getattr(typ, "__fields__", None)
        if fields is not None and len(trm) != len(fields):
            return False
        return True

    def __issub__(typ, other):
        from typed import prop
        from model.mods.check import check

        if not check.every.issub(
            (prop.typeof(typ), prop.typeof(other)),
            STRICT_SCHEMA
        ):
            return False

        return super(STRICT_SCHEMA, typ).__issub__(other)

    def __call__(met, typesystem=None, __check__: bool=None, __extends__=None, **fields):
        if not getattr(met, '__is_base_schema__', False):
            from model.mods.check import require
            require.model.validate(met, fields)
            return dict(**fields)

        from model.mods.resolve import resolve
        from model.mods.check import check
        from typed.mods.types.atomic import Str

        typesystem = resolve.typesystem.entity(typesystem)
        resolved_check = resolve.model.check(__check__)

        bases, _fields, _ = _resolve(met, fields, __extends__=__extends__)

        cache_key = (met, frozenset(_fields.items()), id(typesystem), resolved_check, tuple(__extends__) if __extends__ else None)
        if cache_key in met.__cache__:
            return met.__cache__[cache_key]

        if resolved_check and fields:
            check.every.ismember(set(fields.values()), typesystem)

        display_name = f"StrictSchema({', '.join(f'{k}={typesystem.nameof(v)}' for k, v in _fields.items())})" if _fields else "StrictSchema"

        from model.mods.flags import Flags, ModelFlags
        from typed.mods.init import TYPESYSTEM
        types_set = set(_fields.values()) if _fields else set()

        _display_name = display_name
        _resolved_check = resolved_check
        _typesystems = {TYPESYSTEM, typesystem}

        class StrictSchema(*bases, metaclass=STRICT_SCHEMA):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True, model=ModelFlags(is_schema=True, is_strict=True))
            __typesystems__ = _typesystems
            __display__ = _display_name
            __fields__ = _fields
            __types__ = types_set
            __key_type__ = Str
            __check__ = _resolved_check
            __is_base_schema__ = False

        for k, v in fields.items():
            type.__setattr__(StrictSchema, k, v)

        StrictSchema.__name__ = display_name
        met.__cache__[cache_key] = StrictSchema
        return StrictSchema
