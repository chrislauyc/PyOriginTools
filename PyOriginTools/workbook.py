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

class SHEET:
    def __init__(self,bookName=None,sheetName=None,pull=True):
        """
        create an OR.SHEET object to play with.
        If that book/sheet already exist, the data will be pulled automatically from it.
        If not, a new instance will be created (only in memory).
        """
        self.bookName,self.sheetName=bookName,sheetName
        self.reset() # clear all columns
        if pull: self.pull()

    def __repr__(self):
        """controls what happens when you print() this class."""
        return "PyOriginTools.SHEET [%s]%s (%d cols, %d rows)"%(\
                self.bookName,self.sheetName,self.nCols,self.nRows)

    def reset(self):
        """clears all columns"""
        self.colNames,self.colDesc,self.colUnits,self.colComments,\
        self.colTypes,self.colData=[],[],[],[],[],[]

    ### manipulating columns

    def colAdd(self,name="",desc="",unit="",comment="",coltype=0,data=[],pos=None):
        """
        column types:
            0: Y
            1: Disregard
            2: Y Error
            3: X
            4: Label
            5: Z
            6: X Error
        """
        if pos is None:
            pos=len(self.colNames)
        self.colNames.insert(pos,name)
        self.colDesc.insert(pos,desc)
        self.colUnits.insert(pos,unit)
        self.colComments.insert(pos,comment)
        self.colTypes.insert(pos,coltype)
        self.colData.insert(pos,data)
        return

    def colDelete(self,colI=-1):
        """delete a column at a single index. Negative numbers count from the end."""
#        print("DELETING COLUMN: [%d] %s"%(colI,self.colDesc[colI]))
        self.colNames.pop(colI)
        self.colDesc.pop(colI)
        self.colUnits.pop(colI)
        self.colComments.pop(colI)
        self.colTypes.pop(colI)
        self.colData.pop(colI)
        return

    def onex(self):
        """
        delete all X columns except the first one.
        """
        xCols=[i for i in range(self.nCols) if self.colTypes[i]==3]
        if len(xCols)>1:
            for colI in xCols[1:][::-1]:
                self.colDelete(colI)

    def wiggle(self,noiseLevel=.1):
        """Slightly changes value of every cell in the worksheet. Used for testing."""
        noise=(np.random.rand(*self.data.shape))-.5
        self.data=self.data+noise*noiseLevel

    ### interacting with origin

    def pull(self,bookName=None,sheetName=None):
        """pull data into this OR.SHEET from a real book/sheet in Origin"""

        # tons of validation
        if bookName is None and self.bookName: bookName=self.bookName
        if sheetName is None and self.sheetName: sheetName=self.sheetName
        if bookName is None: bookName=OR.activeBook()
        if bookName and sheetName is None: sheetName=OR.activeSheet()
        if not bookName or not sheetName:
            print("can't figure out where to pull from! [%s]%s"%(bookName,sheetName))
            return

        # finally doing the thing
        poSheet=OR.getSheet(bookName,sheetName)
        self.bookName=bookName
        self.sheetName=sheetName
        self.desc=poSheet.GetLongName()
        self.colNames=[poCol.GetName() for poCol in poSheet.Columns()]
        self.colDesc=[poCol.GetLongName() for poCol in poSheet.Columns()]
        self.colUnits=[poCol.GetUnits() for poCol in poSheet.Columns()]
        self.colComments=[poCol.GetComments() for poCol in poSheet.Columns()]
        self.colTypes=[poCol.GetType() for poCol in poSheet.Columns()]
        self.colData=[poCol.GetData() for poCol in poSheet.Columns()]

    def push(self,bookName=None,sheetName=None,overwrite=False):
        """pull this OR.SHEET into a real book/sheet in Origin"""
        # tons of validation
        if bookName: self.bookName=bookName
        if sheetName: self.sheetName=sheetName
        if not self.sheetName in OR.sheetNames(bookName):
            print("can't find [%s]%s!"%(bookName,sheetName))
            return

        # clear out out sheet by deleting EVERY column
        poSheet=OR.getSheet(bookName,sheetName) # CPyWorksheetPageI
        if not poSheet:
            print("WARNING: didn't get posheet",poSheet,bookName,sheetName)
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
            poSheet.Columns(i).SetData(self.colData[i])

    ### quick refs

    @property
    def nRows(self):
        """returns maximum number of rows based on the longest colData"""
        if self.nCols: return max([len(x) for x in self.colData])
        else: return 0

    @property
    def nCols(self):
        """returns number of columns in the sheet"""
        return len(self.colNames)

    ### managing data with numpy

    @property
    def data(self):
        """return all of colData as a 2D numpy array."""
        data=np.empty((self.nRows,self.nCols),dtype=np.float)
        data[:]=np.nan # make everything nan by default
        for colNum,colData in enumerate(self.colData):
            validIs=np.where([np.isreal(v) for v in colData])[0]
            validData=np.ones(len(colData))*np.nan
            validData[validIs]=np.array(colData)[validIs]
            data[:len(colData),colNum]=validData # only fill cells that have data

        return data

    @data.setter
    def data(self,data):
        """Given a 2D numpy array, fill colData with it."""
        assert type(data) is np.ndarray
        assert data.shape[1] == self.nCols
        for i in range(self.nCols):
            self.colData[i]=data[:,i].tolist()

if __name__=="__main__":
    print("\n"*10)
    t1=time.clock()

    sheet=SHEET(pull=True)
    print(sheet.bookName)
    sheet.wiggle()
    sheet.push(overwrite=True)

#    sheet=SHEET("demoBook","demoSheet",pull=False)
#
#
#    sheet.colAdd(desc='exx',coltype=3,data=np.random.random_sample(np.random.randint(5,15)))
#    sheet.colAdd(desc='why',coltype=0,data=np.random.random_sample(np.random.randint(5,15)))
#
#    print(sheet.data)

#    sheet.colUnits[1]="cuz"
#    sheet.colData[0]=np.array(sheet.colData[0]*1000,dtype=np.int)
#    sheet.push("demoBook","demoSheetA",overwrite=True)

#    sheet.colData[0]=np.array(sheet.colData[0]*1000,dtype=np.int)
#    sheet.desc="newDesc"
#    sheet.push("demoBook","demoSheetB",overwrite=True)
#    sheet.push("demoBook2","lolz",overwrite=True)

    PyOrigin.LT_execute("doc -uw;")
    print("ELAPSED: %.02f ms"%((time.clock()-t1)*1000))