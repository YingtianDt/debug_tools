from debug_tools import DebugMeta
from import_module import Processor
from debug_tools import debug

# class Model(metaclass=DebugMeta):
class Model:
    def __init__(self, name):
        # self.name = name + 1
        self.name = name

    @debug
    def forward(self, x):
        return Processor.process(x)
