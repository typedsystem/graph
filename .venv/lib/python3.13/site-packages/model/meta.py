from typed import lazy

__imports__ = {
    "model.mods.meta.schema": [
        "SCHEMA", "STRICT_SCHEMA", "ORDERED_SCHEMA"
    ],
    "model.mods.meta.model": [
        "MODEL", "STRICT_MODEL", "ORDERED_MODEL",
        "LAZY_MODEL", "LAZY_STRICT_MODEL", "LAZY_ORDERED_MODEL"
    ],
}

if lazy(__imports__):
    from model.mods.types.schema import (
        SCHEMA, STRICT_SCHEMA, ORDERED_SCHEMA
    )
    from model.mods.types.model import (
        MODEL, STRICT_MODEL, ORDERED_MODEL,
        LAZY_MODEL, LAZY_STRICT_MODEL, LAZY_ORDERED_MODEL
    )
