import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

from test_module import Model

model = Model("alexnet")
print(model.forward(5))