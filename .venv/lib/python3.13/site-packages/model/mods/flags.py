from typed.mods.flags import __FLAGS__, Flags as __Flags__, flag as __flag__

class ModelFlags(metaclass=__FLAGS__):
    def __init__(
        self,
        is_model:      bool = False,
        is_strict:     bool = False,
        is_ordered:    bool = False,
        is_schema:     bool = False,
        is_lazy:       bool = False
    ):
        self.is_model = is_model
        self.is_strict = is_strict
        self.is_ordered = is_ordered
        self.is_schema = is_schema
        self.is_lazy = is_lazy

class Flags(__Flags__):
    def __init__(
        self,
        is_discourse: bool=False,
        is_reducer: bool=False,
        is_predicate: bool=False,
        is_evaluator: bool=False,
        is_quantifier: bool=False,
        is_parametric: bool=False,
        is_expression: bool=False,
        is_constructor: bool=False,
        is_dependent: bool=False,
        is_algebraic: bool=False,
        is_enumerable: bool=False,
        is_finite: bool=False,
        is_bounded: bool=False,
        is_extensional: bool=False,
        is_prod: bool=False,
        is_coprod: bool=False,
        is_related: bool=False,
        is_filtered: bool=False,
        model: ModelFlags=None
    ):
        super().__init__(
            is_discourse, is_reducer, is_predicate, is_evaluator, is_quantifier, 
            is_parametric, is_expression, is_constructor, is_dependent, is_algebraic, 
            is_enumerable, is_finite, is_bounded, is_extensional, is_prod, 
            is_coprod, is_related, is_filtered
        )
        if model is None:
            model = ModelFlags()
        self.model = model

class flag(__flag__):
    class model:
        is_model = "is_model"
        is_strict = "is_strict"
        is_ordered = "is_ordered"
        is_schema = "is_schema"
        is_lazy = "is_lazy"
