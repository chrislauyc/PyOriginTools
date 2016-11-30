# PyOriginTools
PyOriginTools is a collection of scripts and examples intended to make life easier for those who want to develop python scripts which interact with OriginLab (and software written in OriginC) using Origin's embedded Python environment using their PyOrigin module. Because the PyOrigin.py that ships with Origin is automatically generated using [SWIG](http://www.swig.org/Doc1.3/Python.html), it is structured a C program (not very pythonic) and cannot be learned intuitively because it is devoid of intrinsic documentation (docstrings) which guide the programmer at the time of coding. The [Official Origin/Python documentation](http://www.originlab.com/doc/python/PyOrigin) is a good start, but not suffecient to learn this object model for those not already familiar with it. 

This module is intended to be installed in a python distribution which [lives somewhere Origin can see it](http://www.originlab.com/doc/LabTalk/guide/work-with-python#A_Note_to_Use_Python_Extensions). It utilizes tools such as numerical analysis tools such as numpy which do not ship with OriginLab.

## Installation
* To install, run ```pip install PyOriginTools```
* To upgrade, run ```pip install --upgrade --no-cache-dir PyOriginTools```

## PyOriginTools.ORIGIN
PyOriginTools.ORIGIN is a class which provides a single layer of abstraction over the complicated (and inconsistent) Origin object model which aims to make most Origin tasks single-line python solutions. All python scripts you run should start like this:

### Example 1: Getting the selected worksheet column names and data

#### Task without PyOriginTools (just stock PyOrigin)
```python
import PyOrigin # <-- this module ships with OriginLab
sheetObject=PyOrigin.ActiveLayer()
columnNames=[x.GetName() for x in sheetObject.Columns()]
columnRows=max([x.GetUpperBound()+1 for x in sheetObject.Columns()])
data=np.empty((columnRows,len(columnNames))) # quickly create array scaffold
data[:]=np.nan # fill it with nans (representing unfilled original data)
for colNum,colData in enumerate([x.GetData() for x in sheetObject.Columns()]):
    data[:len(colData),colNum]=colData
print(columnNames) # list of short names for each column
print(data) # 2D numpy array of all column data
```
####  Task _with_ PyOriginTools
```python
import PyOriginTools.ORIGIN as OR # <-- this is the module you're reading about!
sheet=OR.worksheet() # if the title of a worksheet isn't given, it uses the active one
print(sheet.colNames) # list of short names for each column
print(sheet.data) # 2D numpy array of all column data
```

## PyOrigin.py Documentation
This module comes with an automatically generated HTML outline of PyOrigin.py functions, objects, and their properties. It also comes with inspection reports of common PyOrigin output objects (worksheetPages, worksheetPage, Column, etc.) generated with webinspect.

## Code Examples
The OriginLab website has a few web pages which document PyOrigin in action. I supplement this information with [an extensive flat-file python script](docs/usage examples/examples.py) which can be called from within origin (using `run -pyf "path/to/examples.py"`) that demonstrates many common tasks including:
* listing pages in a project (workbooks, graphs, etc.)
* listing worksheets in workbooks
* listing columns in worksheets
* listing (or setting) details about columns (name, units, comments, etc)
* getting worksheet data from columns, rows, and as 2D numpy arrays
* deleting and creating workbooks
* deleting and creating worksheets
* rearranging the order of worksheets
* adding data to a worksheet (from numpy arrays)
