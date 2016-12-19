"""
Code here relates to high level Origin stuff (things that don't relate)
to individual workbooks, worksheet, graphs, notes, etc. These functions
are intended to do things like list pages, find matching pages, navigate
a project, etc.
"""

# PREPARE TO IMPORT INTELLIGENTLY
import os
import sys
import pickle
import time

if not "../" in sys.path:
    sys.path.append('../') # this helps my IDE be happy
newpath=os.path.abspath(os.path.dirname(os.path.dirname(sys.argv[0])))
if not newpath in sys.path:
    sys.path.append(newpath) # this is really where it's at

# DO THE IMPORTS
import PyOriginTools
import PyOrigin # this is my sham one in my IDE

def pageNames(matching=False,workbooks=True,graphs=True):
    """
    Returns the names of everything (books, notes, graphs, etc.) in the project.

    Args:
        matching (str, optional): if given, only return names with this string in it
        workbooks (bool): if True, return workbooks
        graphs (bool): if True, return workbooks

    Returns:
        A list of the names of what you requested
    """
    # first collect the pages we want
    pages=[]
    if workbooks:
        pages.extend(PyOrigin.WorksheetPages())
    if graphs:
        pages.extend(PyOrigin.GraphPages())

    # then turn them into a list of strings
    pages = [x.GetName() for x in pages]

    # do our string matching if it's needed
    if matching:
        pages=[x for x in pages if matching in x]
    return pages

def bookNames(matching=False):
    """Return a list of the names of all books in the project.

    Args:
        matching (str, optional): if given, only return names with this string in it

    Returns:
        A list of the names of what you requested

    """
    return pageNames(matching,workbooks=True,graphs=False)

def graphNames(matching=False):
    """Return a list of the names of all graphs in the project.

    Args:
        matching (str, optional): if given, only return names with this string in it

    Returns:
        A list of the names of what you requested

    """
    return pageNames(matching,workbooks=False,graphs=True)

def noteNames(matching=False):
    """Return a list of the names of all notes in the project.

    Args:
        matching (str, optional): if given, only return names with this string in it

    Returns:
        A list of the names of what you requested

    """
    return "???" #todo: how do I get this?

def getPage(name):
    """Returns the PyOrigin.Pages() object of the page with that name.
    If that name doesn't exist, None is returned.

    Args:
        name (str): name of the page to get

    Returns:
        PyOrigin.Pages(name) of what you asked for

    """
    if name in pageNames():
        return PyOrigin.Pages(name)
    else:
        return None

def pageFolder(pageName):
    """Returns the full path of the page with that name.
    If that name doesn't exist, None is returned.

    Args:
        name (str): name of the page to get the folder from

    Returns:
        string name of the folder of the page you asked about
    """
    if not pageName in pageNames():
        return None
    return PyOrigin.Pages(pageName).GetFolder().Path()

def getPageType(name,number=False):
    """Returns the type of the page with that name.
    If that name doesn't exist, None is returned.

    Args:
        name (str): name of the page to get the folder from
        number (bool): if True, return numbers (i.e., a graph will be 3)
            if False, return words where appropriate (i.e, "graph")

    Returns:
        string of the type of object the page is
    """
    if not name in pageNames():
        return None
    pageType=PyOrigin.Pages(name).GetType()
    if number:
        return str(pageType)
    if pageType==1:
        return "matrix"
    if pageType==2:
        return "book"
    if pageType==3:
        return "graph"
    if pageType==4:
        return "layout"
    if pageType==5:
        return "notes"

def listEverything(matching=False):
    """Prints every page in the project to the console.

    Args:
        matching (str, optional): if given, only return names with this string in it

    """
    pages=pageNames()
    if matching:
        pages=[x for x in pages if matching in x]
    for i,page in enumerate(pages):
        pages[i]="%s%s (%s)"%(pageFolder(page),page,getPageType(page))
    print("\n".join(sorted(pages)))

def activePath():
    """show the currently selected folder path.

    Returns:
        string of the active folder path
    """
    path=PyOrigin.ActiveFolder().Path()
    return path

def activeBook():
    """Get the name of the currently active book

    Returns:
        name of the active book, or None if no book is active
    """
    try:
        active=PyOrigin.ActivePage()
        assert active.GetType()==2
        return active.GetName()
    except:
        return None

def activeSheet():
    """Get the name of the currently active worksheet (if a book is active)

    Returns:
        name of the active sheet, or None if no book is active
    """
    try:
        active=PyOrigin.ActivePage()
        assert active.GetType()==2
        return PyOrigin.ActiveLayer().GetName()
    except:
        return None

def activeBookAndSheet():
    """Get the the active [book,sheet] (if one is selected)

    Returns:
        a list of the [book,sheet] names (str), or [None,None] if a book isn't selected
    """
    return [activeBook(),activeSheet()]

def sheetNames(book=None):
    """return sheet names of a book.

    Args:
        book (str, optional): If a book is given, pull names from
            that book. Otherwise, try the active one

    Returns:
        list of sheet names (typical case).
        None if book has no sheets.
        False if book doesn't exlist.

    """
    if book:
        if not book.lower() in [x.lower() for x in bookNames()]:
            return False
    else:
        book=activeBook()
    if not book:
        return False
    poBook=PyOrigin.WorksheetPages(book)
    if not len(poBook):
        return None
    return [x.GetName() for x in poBook.Layers()]

def getSheet(book=None,sheet=None):
    """returns the pyorigin object for a sheet."""

    # figure out what book to use
    if book and not book.lower() in [x.lower() for x in bookNames()]:
        print("book %s doesn't exist"%book)
        return
    if book is None:
        book=activeBook().lower()
    if book is None:
        print("no book given or selected")
        return

    # figure out what sheet to use
    if sheet and not sheet.lower() in [x.lower() for x in sheetNames(book)]:
        print("sheet %s doesn't exist"%sheet)
        return
    if sheet is None:
        sheet=activeSheet().lower()
    if sheet is None:
        return("no sheet given or selected")
        print

    # by now, we know the book/sheet exists and can be found
    for poSheet in PyOrigin.WorksheetPages(book).Layers():
        if poSheet.GetName().lower()==sheet.lower():
            return poSheet
    return False

def sheetSelect(book=None,sheet=None):
    """focus on a book/sheet."""
    PyOrigin.LT_execute('page.active$ = "%s";'%sheet) #TODO: remove labtalk!!

def sheetDelete(book=None,sheet=None):
    """
    Delete a sheet from a book. If either isn't given, use the active one.
    """
    if book is None:
        book=activeBook()
    if sheet in sheetNames():
        PyOrigin.WorksheetPages(book).Layers(sheetNames().index(sheet)).Destroy()

def bookCreate(bookName=""):
    """Create an empty workbook."""
    poSheet=PyOrigin.CreatePage(2,bookName,"Origin",1)
    return poSheet.GetName()
    #sheetDeleteEmpty(bookName)

def sheetDeleteEmpty(bookName=None):
    """Delete all sheets which contain no data"""
    if bookName is None:
        bookName = activeBook()
    if not bookName.lower() in [x.lower() for x in bookNames()]:
        print("can't clean up a book that doesn't exist:",bookName)
        return
    poBook=PyOrigin.WorksheetPages(bookName)
    namesToKill=[]
    for i,poSheet in enumerate([poSheet for poSheet in poBook.Layers()]):
        poFirstCol=poSheet.Columns(0)
        if poFirstCol.GetLongName()=="" and poFirstCol.GetData()==[]:
            namesToKill.append(poSheet.GetName())
    for sheetName in namesToKill:
        print("deleting empty sheet",sheetName)
        sheetDelete(bookName,sheetName)

def sheetCreate(bookName=None,sheetName="",sheetDesc="",nSheets=0):
    if bookName is None:
        bookName = activeBook()
    if not bookName:
        print("can't create a sheet without an active book or provided book name.")
        return
    if bookName in bookNames():
        poSheet=PyOrigin.Pages(bookName).AddLayer(sheetName)
        poSheet.SetName(sheetName)
        poSheet.SetLongName(sheetDesc)

def pickle_load(fname):
    """return the contents of a pickle file"""
    assert type(fname) is str and os.path.exists(fname)
    print("loaded",fname)
    return pickle.load(open(fname,"rb"))

def pickle_save(thing,fname=None):
    """save something to a pickle file"""
    if fname is None:
        fname=os.path.expanduser("~")+"/%d.pkl"%time.time()
    assert type(fname) is str and os.path.isdir(os.path.dirname(fname))
    pickle.dump(thing, open(fname,"wb"),pickle.HIGHEST_PROTOCOL)
    print("saved",fname)


def sheetToHTML(sheet):
    """
    Put 2d numpy data into a temporary HTML file.
    This is a hack, copy/pasted from an earlier version of this software.
    It is very messy, but works great! Good enough for me.
    """

    assert "SHEET" in str(type(sheet))
    #data,names=None,units=None,bookName=None,sheetName=None,xCol=None
    #sheet=OR.SHEET()
    data=sheet.data
    names=sheet.colDesc
    units=sheet.colUnits
    bookName=sheet.bookName
    sheetName=sheet.sheetName

    def htmlListToTR(l,trClass=None,tdClass=None,td1Class=None):
        """
        turns a list into a <tr><td>something</td></tr>
        call this when generating HTML tables dynamically.
        """
        html="<tr>"
        for item in l:
            html+="<td>%s</td>"%item
        html+="</tr>"
        if trClass:
            html=html.replace("<tr>",'<tr class="%s">'%trClass)
        if td1Class:
            html=html.replace("<td>",'<td class="%s">'%td1Class,1)
        if tdClass:
            html=html.replace("<td>",'<td class="%s">'%tdClass)
        return html

    htmlFname = os.path.expanduser("~")+"/WKS-%s.%s.html"%(bookName,sheetName)
    html="""<body>
    <style>
    body {
          background-color: #ababab;
          padding:20px;
          }
    table {
           font-size:12px;
           border-spacing: 0;
           border-collapse: collapse;
           }
    .name {background-color:#fafac8;text-align:center;}
    .units {background-color:#fafac8;text-align:center;}
    .data0 {background-color:#FFFFFF;font-family: monospace;text-align:center;}
    .data1 {background-color:#FAFAFA;font-family: monospace;text-align:center;}
    .labelRow {background-color:#e0dfe4; text-align:right;border:1px solid #000000;}
    .labelCol {background-color:#e0dfe4; text-align:center;border:1px solid #000000;  padding-left: 20px; padding-right: 20px;}
    td {
        border:1px solid #c0c0c0; padding:5px;
        font-family: Arial, Helvetica, sans-serif;
        }
    </style>
    <html>"""
    html+="<h1>FauxRigin</h1>"
    if bookName or sheetName:
        html+='<code><b>%s / %s</b></code><br><br>'%(bookName,sheetName)
    html+="<table>"
    colNames=['']
    for i in range(len(units)):
        shortName=chr(i%26+ord('A'))
        if i>=26:
            shortName=chr(int(i/26-1)+ord('A'))+shortName
        label="%s(%s)"%(shortName,"X" if sheet.colTypes[i]==3 else "Y")
        colNames.append(label)
    html+=htmlListToTR(colNames,'labelCol','labelCol')
    html+=htmlListToTR(['Long Name']+list(names),'name',td1Class='labelRow')
    html+=htmlListToTR(['Units']+list(units),'units',td1Class='labelRow')
    cutOff=False
    for y in range(len(data)):
        html+=htmlListToTR([y+1]+list(data[y]),trClass='data%d'%(y%2),td1Class='labelRow')
        if y>=200:
            cutOff=True
            break
    html+="</table>"
    html=html.replace(">nan<",">--<")
    html=html.replace(">None<","><")
    if cutOff:
        html+="<h3>... showing only %d of %d rows ...</h3>"%(y,len(data))
    html+="</body></html>"
    with open(htmlFname,'w') as f:
        f.write(html)
    import webbrowser
    webbrowser.open(htmlFname)
    return

if __name__=="__main__":
    print("DO NOT RUN THIS SCRIPT DIRECTLY.")
    print("Version",PyOriginTools.__version__)
    print("active:",activeBookAndSheet())