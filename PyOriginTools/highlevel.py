"""
Code here relates to high level Origin stuff (things that don't relate)
to individual workbooks, worksheet, graphs, notes, etc. These functions
are intended to do things like list pages, find matching pages, navigate
a project, etc.
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
        if not book in bookNames():
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
    if book and not book in bookNames():
        print("book %s doesn't exist"%book)
        return
    if book is None:
        book=activeBook()
    if book is None:
        print("no book given or selected")
        return

    # figure out what sheet to use
    if sheet and not sheet in sheetNames(book):
        print("sheet %s doesn't exist"%sheet)
        return
    if sheet is None:
        sheet=activeSheet()
    if sheet is None:
        return("no sheet given or selected")
        print

    # by now, we know the book/sheet exists and can be found
    for poSheet in PyOrigin.WorksheetPages(book).Layers():
        if poSheet.GetName()==sheet:
            return poSheet
    return False

def sheetDelete(book=None,sheet=None):
    """
    Delete a sheet from a book. If either isn't given, use the active one.
    """
    if book is None:
        book=activeBook()
    if sheet in sheetNames():
        PyOrigin.WorksheetPages(book).Layers(sheetNames().index(sheet)).Destroy()


if __name__=="__main__":
    print("DO NOT RUN THIS SCRIPT DIRECTLY.")
    print("Version",PyOriginTools.__version__)
    print("active:",activeBookAndSheet())