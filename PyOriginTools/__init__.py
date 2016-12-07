"""
# ONE THIS ONCE IN ORIGIN:
import sys, imp;\
bak_modules = sys.modules.copy();\
sys.argv=['./'];\
sys.path.append('C:/Users/swharden/Documents/GitHub/PyOriginTools');\

# THIS WILL RELOAD THE CODE:
for k in sys.modules.keys():
    if not k in bak_modules:
        del sys.modules[k]
import PyOriginTools

print("PyOriginTools version:",PyOriginTools.__version__)
"""

from PyOriginTools.version import __version__

from PyOriginTools.highlevel import *
from PyOriginTools.workbook import *