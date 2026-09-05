def _sizeof(self, attr):
    return len(getattr(self, "__nodes__", set())) + len(getattr(self, attr, set()))

def _loopsof(self, attr):
    return {e for e in getattr(self, attr, set()) if len(set(getattr(e, "__nodes__", []))) == 1}
