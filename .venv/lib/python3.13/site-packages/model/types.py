from typed import lazy

__imports__ = {
    "model.mods.types.schema": [
        "Schema", "StrictSchema", "OrderedSchema"
    ],
    "model.mods.types.model": [
        "Model", "StrictModel", "OrderedModel",
        "LazyModel", "LazyStrictModel", "LazyOrderedModel"
    ],
}

if lazy(__imports__):
    from model.mods.types.schema import (
        Schema, StrictSchema, OrderedSchema
    )
    from model.mods.types.model import (
        Model, StrictModel, OrderedModel,
        LazyModel, LazyStrictModel, LazyOrderedModel
    )
