r"""
run -pyf C:\Users\swharden\Documents\GitHub\PyOriginTools\documentation\demonstrations\basics.py
"""

import sys
if False:
    # this code block will NEVER actually run
    sys.path.append('../../') # helps my IDE autocomplete

import PyOriginTools as OR

if __name__=="__main__":
    if all(OR.activeBookAndSheet()):
        print(OR.activeBookAndSheet())
    else:
        print("a book is not selected")