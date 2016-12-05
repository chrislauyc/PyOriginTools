r"""
When developing, load or reload PyOriginTools by calling:
run -pyf C:\Users\swharden\Documents\GitHub\PyOriginTools\PyOriginTools\load.py
"""

import sys
path='C:/Users/swharden/Documents/GitHub/PyOriginTools'
if not "PyOriginTools" in dir():
    # this is our first load
    if not path in sys.path:
        sys.path.append(path)
    bak_modules = sys.modules.copy()
    print("remembering original modules...")
else:
    # a reload is needed
    modulesToKill=[x for x in sys.modules.keys() if not x in bak_modules]
    print("killing %d modules..."%len(modulesToKill))
    for name in modulesToKill:
            del sys.modules[name]
import PyOriginTools