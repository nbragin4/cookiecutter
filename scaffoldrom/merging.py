"""Strategy configuration for merging two context files"""
from copy import deepcopy
from deepmerge import Merger

def strategy_default(config, path, base, nxt):
    """check if it default list"""
    if len(base) == 1 and isinstance(base[0], dict):
        merged = [config.value_strategy(path + [v], deepcopy(base[0]), v) for v in nxt]
        return merged
    return nxt

merger: Merger = Merger([(list,[strategy_default]),(dict,["merge"])],["override"],["override"])
