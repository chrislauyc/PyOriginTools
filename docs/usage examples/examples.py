"""
This script is intended to demonstrate how to interact with PyOrigin
when a script is called from within OriginLab (tested in Origin 2017).

USING IDES THAT SUPPORT AUTOCOMPLETE:
    I grabbed PyOrigin.py from the Origin program files folder and
    placed it in the Python35/Lib/ folder. I modified the entire
    file and placed all its contents inside an "if False:" statement
    so none of it gets run. However, just having it there lets me
    access its object model in smart python IDEs.

TO RUN THIS SCRPIT: open a CLEAN origin session and type this into Origin:
    run -pyf "C:\path\to\PyOrigin_examples.py" runall

(if you get import errors, make sure all modules are pip-installed)
"""

import os
import sys
import PyOrigin # this is my sham one in my IDE
import traceback
import numpy as np
import time
#import webinspect
#webinspect.blacklist.append("GetTheme") # running GetTheme() crashes Origin

### internal routines
# you don't need to worry about this

if "__file__" in dir():
    print("call this from Origin by running:")
    print('run -pyf "%s"'%os.path.abspath(__file__))
    print("or to run every test:")
    print('run -pyf "%s" runall'%os.path.abspath(__file__))
else:
    print("it looks like you're calling this from inside Origin")

def exceptionToString(e,silent=False):
    """when you "except Exception as e", give me the e and I'll give you a string."""
    exc_type, exc_obj, exc_tb = sys.exc_info()
    s=("\n"+"="*50+"\n")
    s+="EXCEPTION THROWN UNEXPECTEDLY\n"
    s+="  FILE: %s\n"%os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    s+="  LINE: %s\n"%exc_tb.tb_lineno
    s+="  TYPE: %s\n"%exc_type
    s+='-'*50+'\n'
    s+=traceback.format_exc()
    s=s.strip()+'\n'+"="*50+"\n"
    if not silent:
        print(s)
    return s

### Origin Examples

def demo_000_showPaths():
    print("This is where Origin is looking when 'import' statements are used:")
    print("\n".join(sys.path))
    return

### GET WORKBOOKS, WORKSHEETS, AND ADD DATA

def demo_100_createBook():

    print("starting by destroyold and old 'SWHdemo' books...")
    PyOrigin.DestroyPage('SWHdemo')
    print("now creating a 'SWHdemo' book from scratch...")
    worksheetPage=PyOrigin.CreatePage(2,"","Origin",1) # 2 means worksheet, 1 means not hidden
    print("short name was:",worksheetPage.GetName()) # automatically assigned
    worksheetPage.SetName("SWHdemo")
    print("short name is now:",worksheetPage.GetName()) # must be unique
    worksheetPage.SetLongName("fancy pancy empty workbook") # doesn't have to be unique
    print("number of sheets:",worksheetPage.Layers().GetCount()) # 1 sheet = 1 layer?

def demo_101_addSheet():
    page=PyOrigin.Pages('SWHdemo')
    sheet=page.AddLayer('SheetDemo') # creates sheet and returns it
    bookName,sheetName,sheetIndex=sheet.GetPage().GetName(),sheet.GetName(),sheet.GetIndex()
    print('created [{}]{} (index {})'.format(bookName,sheetName,sheetIndex))
    sheet.SetIndex(0) # moves this sheet to the front

def demo_102_populateSheet():
    worksheetPage=PyOrigin.WorksheetPages("SWHdemo") # this is the workbook name
    worksheetPage.SetLongName("dummy data") # doesn't have to be unique
    firstSheet=worksheetPage.Layers(0) #CPyWorksheet

    # add and delete columns
    print("number of columns before:",firstSheet.GetColCount())
    for i in range(10):
        colname="newCol%d"%i # will change if not unique
        print('  adding a column: "SWH" at position 1...')
        firstSheet.InsertCol(1,colname) # position, shortName
    print("number of columns now:",firstSheet.GetColCount())
    for i in range(5):
        print('  deleting column 1...')
        firstSheet.DeleteCol(1) # position
    print("deleting all but 5 rows one by one...")
    print("number of columns now:",firstSheet.GetColCount())

    # add some data
    for colNum,columnObject in enumerate(firstSheet.Columns()):
        columnObject.SetName("Scott%d"%colNum)
        columnObject.SetLongName("neuron %d"%colNum)
        columnObject.SetComments("16.%d.abf"%colNum)
        columnObject.SetUnits("spines")
        data=list(np.arange(50)*(colNum+1)) # generate incrementally increasing data
        data=data+np.round(np.random.random_sample(len(data)),2) # add noise
        print("  filling column",colNum,'with',data)
        columnObject.SetData(data)

    # modifying rows works the same way
    for i in range(5):
        print("deleting row",10+i)
        firstSheet.DeleteRow(10) # position


### GET WORKBOOK/WORKSHEET INFO

def demo_201_inspect_workbooks():
    print("gives details for all workbooks in the project")
    print("Worksheet Pages:")
    print("\n".join(["  "+page.GetName() for page in PyOrigin.WorksheetPages()]))

def demo_202_inspect_graphs():
    print("gives details for all graphs in the project")
    print("(there may not be any!)")
    for page in PyOrigin.GraphPages():
        print(page.GetFolder(),page.GetName())

def demo_202_inspect_pages():
    print("gives details for all pages (graphs and worksheets) in the project")
    for page in PyOrigin.GraphPages():
        print("Type: {} Name: {}".format(page.GetType(),page.GetName()))

def demo_203_list_pages():
    print("listing all pages (graphs and worksheets) in the project by their name")
    pages_all=[x.GetName() for x in PyOrigin.Pages()]
    pages_worksheets=[x.GetName() for x in PyOrigin.Pages() if x.GetType()==2]
    pages_graph=[x.GetName() for x in PyOrigin.Pages() if x.GetType()==3]
    print("PAGES:",pages_all)
    print("WORKSHEETS:",pages_worksheets)
    print("GRAPHS:",pages_graph)

def demo_204_active():
    print("showing basics about what's active.")
    print("PyOrigin.ActiveFolder():",PyOrigin.ActiveFolder())
    print("PyOrigin.ActiveFolder().Path():",PyOrigin.ActiveFolder().Path())
    print("PyOrigin.ActiveLayer():",PyOrigin.ActiveLayer())
    try:
        print("PyOrigin.ActivePage():",PyOrigin.ActivePage())
    except:
        print("PyOrigin.ActivePage(): CRASHED!!!! Does that when notes are selected.")

def demo_205_list_workbook_sheets():
    print("selecting a worksheet page by its name")

    # find names of workbooks so we can select one by name
    worksheetNames=[x.GetName() for x in PyOrigin.WorksheetPages()]
    print("workbooks available (oldest to newest):",worksheetNames)
    assert len(worksheetNames) # don't let it continue if it didn't find any
    workbookName=worksheetNames[0] # you could manually set this, i.e., 'EventsEp2'
    print('selecting oldest workbook by its name: "%s"'%workbookName)

    # select the workbook and list sheets
    workbook=PyOrigin.WorksheetPages(workbookName)
    sheetNames=[x.GetName() for x in workbook.Layers()]
    print("found %d sheets:"%len(sheetNames))
    for i,worksheetName in enumerate(sheetNames):
        print('PyOrigin.WorksheetPages("{}").Layers({}) will select {} sheet'.format(workbookName,i,worksheetName))

def demo_206_active_worksheet_info():
    print("showing info on the currently selected sheet of the active workbook")
    # figure out the last selected book/sheet
    # note that these stay "active" even if note objects are selected.
    print("This page name is:",PyOrigin.ActiveLayer().GetPage())
    print("This page type is:",PyOrigin.ActiveLayer().GetPage().GetType())
    if not PyOrigin.ActiveLayer().GetPage().GetType()==2:
        print("this type isn't what it's supposed to be (2 for worksheet). aborting.")
        return

    # collect and show information about the sheet and index we have selected
    bookName=PyOrigin.ActiveLayer().GetPage()
    sheetName=PyOrigin.ActiveLayer().GetName()
    sheetIndex=PyOrigin.ActiveLayer().GetIndex()
    print('active book: "{}"'.format(bookName))
    print('active sheet: "{}" (index: {})'.format(sheetName,sheetIndex))

    # show information about the names and data it contains
    sheetObject=PyOrigin.ActiveLayer()
    columnSNs=[x.GetName() for x in sheetObject.Columns()]
    columnLNs=[x.GetLongName() for x in sheetObject.Columns()]
    columnData=[x.GetData() for x in sheetObject.Columns()] # too much to show
    columnDataLengths=[len(x) for x in columnData]
    columnTypes=[x.GetType() for x in sheetObject.Columns()]
    columnTypes2=str(columnTypes).replace("3","X").replace("0","Y")
    columnCount=len(columnSNs)
    columnRows=max([x.GetUpperBound()+1 for x in sheetObject.Columns()])
    columnRows=max(columnDataLengths) # would also work if GetData() already ran
    print("I see {} columns with {} rows".format(columnCount,columnRows))
    print("column short names:",columnSNs)
    print("column long names:",columnLNs)
    print("column types:",columnTypes2)
    print("column data lengths:",columnDataLengths)
    print("the last column contains data:",columnData[-1])

def demo_207_active_worksheet_data_numpy():
    print("convertinng data of the selected worksheet to a 2D numpy array")
    if not PyOrigin.ActiveLayer().GetPage().GetType()==2:
        print("a worksheet should be selected! aborting.")
        return
    print("WARNING: this may crash if you have letters in your document.")
    sheetObject=PyOrigin.ActiveLayer()
    columnCount=len([x for x in sheetObject.Columns()])
    columnRows=max([x.GetUpperBound()+1 for x in sheetObject.Columns()])

    # let's do the numpy stuff now!
    data=np.empty((columnRows,columnCount)) # quickly create array scaffold
    # if you were to want to accept letters, specify dtype=np.object in np.empty()
    data[:]=np.nan # fill it with nans (representing unfilled original data)
    for colNum,colData in enumerate([x.GetData() for x in sheetObject.Columns()]):
        # data[x] is data[x,:] and represents rows
        # data[:][x] is data[:,x] and represents columns
        # data[:] would mean fill every row (we might not have that much data)
        # data[:len(colData)] means fill only up to the size of colData
        data[:len(colData),colNum]=colData

    # now it's all processed. show it in different ways.
    print("\n\nFancy numpy array:")
    print(data)

    print("\n\nPrinting line by (x,y) coordinates (to row 5):")
    for row in range(data.shape[0]):
        if row<5:
            for col in range(data.shape[1]):
                print("row: {}, col: {}, cell={}".format(row,col,data[row,col]))

    print("\n\nPrinting line by (x,y) coordinates (to row 5):")
    for row in range(data.shape[0]):
        if row<5:
            for col in range(data.shape[1]):
                print("{:>7.02f}\t".format(data[row,col]),end="") # no end line break
            print() # force end line break after each row

def demo_999_redrawScreen():
    print("refreshing the Origin window")
    #TODO: is there a PyOrigin way to do this?
    PyOrigin.LT_execute("doc -uw;")

if __name__=="__main__":
    # this will CRASH if you don't run it from WITHIN origin with run -pyf
    if 'runall' in str(sys.argv):
        print("\n\n\n"+"#"*50+"\n# RUNNING ATUOMATED TEST SEQUENCE\n"+"#"*50+"\n\n\n")
        for functionName in [x for x in sorted(globals()) if x.startswith("demo_")]:
            print("\n####### {}() #######".format(functionName))
            t1=time.clock()
            try:
                globals()[functionName]()
            except Exception as e:
                exceptionToString(e)
                break
            print("finished in %.02f milliseconds."%((time.clock()-t1)*1000))
            demo_999_redrawScreen()
    else:
        demo_999_redrawScreen()


    print("DONE")
