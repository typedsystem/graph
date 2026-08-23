from model.mods.meta.model import (
    MODEL, ORDERED_MODEL, STRICT_MODEL,
    LAZY_MODEL, LAZY_ORDERED_MODEL, LAZY_STRICT_MODEL
)
from model.mods.flags import Flags, ModelFlags
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from model.mods.types.schema import Schema

class Model(metaclass=MODEL):
    __flags__ = Flags(is_constructor=True, model=ModelFlags(is_model=True))
    __is_base_model__ = True

    @classmethod
    def schema(cls) -> 'Type[Schema]':
        from model.mods.func import schema as _schema
        return _schema(cls)

class OrderedModel(Model, metaclass=ORDERED_MODEL):
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_ordered=True))
    __is_base_model__ = True

class StrictModel(Model, metaclass=STRICT_MODEL):
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_strict=True))
    __is_base_model__ = True

class LazyModel(Model, metaclass=LAZY_MODEL):
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_lazy=True))
    __is_base_model__ = True

class LazyOrderedModel(LazyModel, OrderedModel, metaclass=LAZY_ORDERED_MODEL):
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_lazy=True, is_ordered=True))
    __is_base_model__ = True

class LazyStrictModel(LazyModel, StrictModel, metaclass=LAZY_STRICT_MODEL):
    __flags__   = Flags(is_constructor=True, model=ModelFlags(is_model=True, is_lazy=True, is_strict=True))
    __is_base_model__ = True
