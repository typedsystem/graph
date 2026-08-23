def _traverse(val, callback):
    from model.mods.check import check
    if check.model.ismodel(val):
        return callback(val)
    elif check.model.ismodel(type(val)):
        return callback(val)
    elif isinstance(val, list):
        return [_traverse(v) for v in val]
    elif isinstance(val, dict):
        return {k: _traverse(v) for k, v in val.items()}
    elif isinstance(val, tuple):
        return tuple(_traverse(v) for v in val)
    return val
