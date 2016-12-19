R"""
try to get the worksheet name from a worksheet
run -pyf C:\Users\swharden\Documents\GitHub\PyOriginTools\documentation\demonstrations\abfFromWks.py
"""

import sys
if False:
    # this code block will NEVER actually run
    sys.path.append('../') # helps my IDE autocomplete
    sys.path.append('../../') # helps my IDE autocomplete
    sys.path.append('../../../') # helps my IDE autocomplete

import PyOriginTools as OR
import PyOrigin

if __name__=="__main__":
    bookName,sheetName=OR.activeBookAndSheet()
    worksheetPage=PyOrigin.WorksheetPages(bookName)
    print(worksheetPage[0])
#    for item in worksheetPage:
#        print(item)
    print("DONE")