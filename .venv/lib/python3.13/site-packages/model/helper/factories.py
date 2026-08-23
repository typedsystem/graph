import json
from typed import List

def _extends(__extends__):
    extends = []
    if __extends__:
        if __extends__ in List:
            extends.extend(__extends__)
        else:
            extends.append(__extends__)

    return [m.materialize() if getattr(m, "is_lazy", False) else m for m in extends]

def _json(obj):
    from model.mods.types import Model, Lazy
    json_dict = {}
    for key, value in obj.__dict__.items():
        if key.startswith('_'):
            continue
        if value in Model or value in Lazy:
            json_dict[key] = _json(value)
        elif isinstance(value, list) and all(item in Model or item in Lazy for item in value):
            json_dict[key] = [_json(item) for item in value]
        elif isinstance(value, dict) and any(item in Model or item in Lazy for item in value.values()):
            processed_dict = {}
            for sub_key, sub_value in value.items():
                if sub_value in Model or sub_value in Lazy:
                    processed_dict[sub_key] = _json(sub_value)
                else:
                    processed_dict[sub_key] = sub_value
            json_dict[key] = processed_dict
        else:
            try:
                json.dumps(value)
                json_dict[key] = value
            except TypeError:
                json_dict[key] = str(value)
    return json_dict
