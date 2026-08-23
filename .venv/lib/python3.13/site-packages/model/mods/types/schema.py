from model.mods.meta.schema import (
    SCHEMA, ORDERED_SCHEMA, STRICT_SCHEMA,
)
from model.mods.flags import Flags, ModelFlags
from typing import Dict, Any

class Schema(metaclass=SCHEMA):
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_schema=True))
    __is_base_schema__ = True
    __null__    = {}
    __builtin__ = dict

    def __size__(trm):
        return len(trm)

    def __getitem__(trm, key):
        return trm.__dict__[key]

    def __setitem__(trm, key, value):
        from typed import check, prop
        fields = getattr(prop.typeof(trm), '__fields__', {})
        if key in fields:
            check.isterm(value, fields[key])
        trm.__dict__[key] = value

    def __contains__(trm, key):
        return key in trm.__dict__

    @classmethod
    def unwrap(cls) -> Dict[str, Any]:
        from model.mods.func import unwrap as _unwrap
        return _unwrap(cls)

class OrderedSchema(Schema, metaclass=ORDERED_SCHEMA):
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_schema=True, is_ordered=True))
    __is_base_schema__ = True
    __null__    = {}
    __builtin__ = dict

class StrictSchema(Schema, metaclass=STRICT_SCHEMA):
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_schema=True, is_strict=True))
    __is_base_schema__ = True
    __null__    = {}
    __builtin__ = dict
