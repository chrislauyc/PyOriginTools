"""
scratch pad for functin ideas.
DONT LET THINGS SIT IN HERE FOR LONG!
"""

# PREPARE TO IMPORT INTELLIGENTLY
import os
import sys
if not "../" in sys.path:
    sys.path.append('../') # this helps my IDE be happy
newpath=os.path.abspath(os.path.dirname(os.path.dirname(sys.argv[0])))
if not newpath in sys.path:
    sys.path.append(newpath) # this is really where it's at

# DO THE IMPORTS
import PyOriginTools as OR
import PyOrigin # this is my sham one in my IDE
import webinspect
import time

class BOOK:
    def __init__(self,bookName=None,pull=True):
        """
        load every worksheet in a workbook into memory.
        useful for things like getcols and across-sheet-stats.

        #TODO: preserve order of sheets by using index/order value
        """
        if bookName is None:
            bookName=OR.activeBook()
            self.bookName = bookName
        if pull and bookName in OR.bookNames():
            self.pull(bookName)
        else:
            self.bookName=bookName
            self.sheets=[] # OR.SHEET objects
            self.sheetNames=[]

    def pull(self,bookName=None):
        if bookName is None:
            bookName=OR.activeBook()
        if bookName is None or not bookName in OR.bookNames():
            print("that book doesn't exist.")
            return

        self.sheets=[]
        print("pulling [%s]..."%bookName)
        t1=time.clock()
        self.sheetNames=OR.sheetNames(bookName)
        for sheetName in self.sheetNames:
            self.sheets.append(OR.SHEET(bookName,sheetName))
        print("loaded %d sheets in memory (%.02f ms)"%(len(self.sheets),(time.clock()-t1)*1000))


def getcols(sheetMatch=None,colMatch="Decay"):
    """find every column in every sheet and put it in a new sheet or book."""
    book=BOOK()
    if sheetMatch is None:
        matchingSheets=book.sheetNames
        print('all %d sheets selected '%(len(matchingSheets)))
    else:
        matchingSheets=[x for x in book.sheetNames if sheetMatch in x]
        print('%d of %d sheets selected matching "%s"'%(len(matchingSheets),len(book.sheetNames),sheetMatch))
    matchingSheetsWithCol=[]
    for sheetName in matchingSheets:
        i = book.sheetNames.index(sheetName) # index of that sheet
        for j,colName in enumerate(book.sheets[i].colDesc):
            if colMatch in colName:
                matchingSheetsWithCol.append((sheetName,j))
                break
        else:
            print("  no match in [%s]%s"%(book.bookName,sheetName))
    print("%d of %d of those have your column"%(len(matchingSheetsWithCol),len(matchingSheets)))
    for item in matchingSheetsWithCol:
        print(item,item[0],item[1])

if __name__=="__main__":
    print("DO NOT RUN THIS SCRIPT DIRECTLY.")
    print("Version",OR.__version__)
    t1=time.clock()

    getcols(sheetMatch="_")
    #getcols()

    PyOrigin.LT_execute("doc -uw;")
    print("ELAPSED: %.02f ms"%((time.clock()-t1)*1000))