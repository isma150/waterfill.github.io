"""Stable numeric ids for named UI instances (used as the 'id' instance variable)."""
_reg = {}
def nid(name):
    if name not in _reg:
        _reg[name] = len(_reg) + 1
    return _reg[name]
def all_ids():
    return dict(_reg)
