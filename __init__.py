import sys
import types
import importlib
from . import logger
from functools import wraps

logger = logger.Logger("DEBUG TOOL")

def reload(symbol):
    module_name = symbol.__module__
    names = symbol.__qualname__.split(".")
    ret = importlib.reload(sys.modules[module_name]) 
    for name in names:
        ret = getattr(ret, name)
    return ret

def process_err(err):
    import traceback
    exc_type, exc_value, tb = sys.exc_info()
    tb_info = traceback.extract_tb(tb)
    logger.log("Error encountered.")
    logger.log("Traceback:")
    logger.log("".join(traceback.format_list(tb_info)))
    logger.log(err)
    logger.log('')
    return tb
    


def debug(method):
    @wraps(method)
    def wrapper(*args, **kwargs):

        def process_option(option):
            if option in ["q", "quit"]: exit(); return True
            elif option in ["d", "debug"]: logger.log("PDB debugger opened..."); import pdb; pdb.post_mortem(tb); return True
            elif option in ["c", "continue"]: return True
            elif option.startswith("r"):
                # reload any symbol in the current module, even if the symbol is imported from elsewhere
                symbol_str = option.split()[-1]
                module = sys.modules[method.__module__]
                symbol = getattr(module, symbol_str)
                reload(symbol)
                return False
            else: print("Invalid option. Please try again."); return False

        original_method = method
        while True:
            try:
                return original_method(*args, **kwargs)
            except Exception as err:
                tb = process_err(err)
                while True:
                    option = input("[OPTION]:")
                    cont = process_option(option)
                    if cont:
                        break
                original_method = reload(original_method)

    return wrapper


class DebugMeta(type):
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, types.FunctionType):
                attrs[attr_name] = debug(attr_value)
        return super().__new__(cls, name, bases, attrs)
