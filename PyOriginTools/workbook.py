r"""
code related to creating, inspecting, and modifying workbooks.

I test this via:
run -pyf C:\Users\swharden\Documents\GitHub\PyOriginTools\PyOriginTools\load.py;
run -pyf C:\Users\swharden\Documents\GitHub\PyOriginTools\PyOriginTools\workbook.py

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
import numpy as np

class BOOK:
    def __init__(self,name=None):
        """
        create an OR.BOOK object to play with.

        Args:
            shortName (str): the short name of the book. If this does
                not exist in the project, it will be created. If this
                does exist, it will pull data from the project book
        """
        if not name:
            self.name="B"+str(int(time.time()))[-7:]

class SHEET:
    def __init__(self,pullBook=None,pullSheet=None):
        """
        create an OR.SHEET object to play with.
        """

        if pullBook in OR.bookNames() and pullSheet in OR.sheetNames(pullBook):
            self.pull(pullBook,pullSheet)
        else:
            self.book=None
            self.name=None
            self.colNames=None
            self.colDesc=None
            self.colUnits=None
            self.colComments=None
            self.colTypes=None
            self.data=None
            print("ignoring inputs and creating a totally empty OR.SHEET")

    def pull(self,bookName,sheetName):
        """pull data into this OR.SHEET from a real book/sheet in Origin"""
        poSheet=OR.getSheet(bookName,sheetName)
        self.book=bookName
        self.name=poSheet.GetName()
        self.colNames=[poCol.GetName() for poCol in poSheet.Columns()]
        self.colDesc=[poCol.GetLongName() for poCol in poSheet.Columns()]
        self.colUnits=[poCol.GetUnits() for poCol in poSheet.Columns()]
        self.colComments=[poCol.GetComments() for poCol in poSheet.Columns()]
        self.colTypes=[poCol.GetType() for poCol in poSheet.Columns()]
        columnCount=len(self.colNames)
        columnRows=max([x.GetUpperBound()+1 for x in poSheet.Columns()])
        self.data=np.empty((columnRows,columnCount))
        self.data[:]=np.nan # empty cells will be nan
        for colNum,colData in enumerate([x.GetData() for x in poSheet.Columns()]):
            self.data[:len(colData),colNum]=colData
        print("[%s]%s yielded %d columns with %d rows (%d cells)"%(bookName,
              sheetName,columnCount,columnRows,self.data.size,))

    def push(self,bookName=None,sheetName=None):
        """pull this OR.SHEET into a real book/sheet in Origin"""
        if bookName is None:
            bookName=self.book
        if sheetName is None:
            sheetName=self.name

        # clear out out sheet by deleting EVERY column
        poSheet=OR.getSheet(bookName,sheetName) # CPyWorksheetPageI
        for poCol in [x for x in poSheet if x.IsValid()]:
            poCol.Destroy()

        # create columns and assign properties to each
        for i in range(len(self.colNames)):
            poSheet.InsertCol(i,self.colNames[i])
            poSheet.Columns(i).SetName(self.colNames[i])
            poSheet.Columns(i).SetLongName(self.colDesc[i])
            poSheet.Columns(i).SetUnits(self.colUnits[i])
            poSheet.Columns(i).SetComments(self.colComments[i])
            poSheet.Columns(i).SetType(self.colTypes[i])
            poSheet.Columns(i).SetData(self.data[:,i])

def sheetPull(bookName=None,sheetName=None):
    """intelligently pull a sheet. If book or name isn't given, the active ones
    are used. If no book or sheet is selected, or if the sheet isn't in the book,
    None is returned."""
    if bookName is None:
        bookName=OR.activeBook()
    if not bookName or not bookName in OR.bookNames():
        return None
    if not sheetName:
        sheetName=OR.activeSheet()
    if not sheetName or not sheetName in OR.sheetNames(bookName):
        return None
    return SHEET(bookName,sheetName)

if __name__=="__main__":
    t1=time.clock()
    sheet=sheetPull() # pull a sheet's data
    sheet.data=sheet.data*(.5+np.random.random()) # modify the data
    sheet.push() # push it back in
    PyOrigin.LT_execute("doc -uw;")
    print("ELAPSED: %.02f ms"%((time.clock()-t1)*1000))