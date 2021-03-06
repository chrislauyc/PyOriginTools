***WARNING: THIS PROJECT IS ABANDONWARE!*** Although a lot of effort was initially invested in this project, I decided just to perform all data analysis for my own needs in pure Python. PyOriginTools relies somewhat on [SWHLab](https://github.com/swharden/SWHLab) which I have since replaced with [pyABF](https://github.com/swharden/pyABF). I have stopped maintaining PyOriginTools (which tends to break as new Origin versions are released), and am leaving it up to the core OriginLab developers to improve Python support (and documentation) to the point where it's intuitive and functional. Code has been left here intact for backup and educational purposes.

---

# PyOriginTools
PyOriginTools is a collection of scripts and examples intended to make life easier for those who want to develop python scripts which interact with OriginLab (and software written in OriginC) using Origin's embedded Python environment using their PyOrigin module. Because the PyOrigin.py that ships with Origin is automatically generated using SWIG (http://www.swig.org/Doc1.3/Python.html), it is structured a C program (not very pythonic) and cannot be learned intuitively because it is devoid of intrinsic documentation (docstrings) which guide the programmer at the time of coding. The Official Origin/Python documentation (http://www.originlab.com/doc/python/PyOrigin) is a good start, but not suffecient to learn this object model for those not already familiar with it. 

This module is intended to be installed in a python distribution which [lives somewhere Origin can see it](http://www.originlab.com/doc/LabTalk/guide/work-with-python#A_Note_to_Use_Python_Extensions). It utilizes tools such as numerical analysis tools such as numpy which do not ship with OriginLab.

## Installation
* To install, run ```pip install PyOriginTools```
* To upgrade, run ```pip install --upgrade --no-cache-dir --no-dependencies PyOriginTools```

## Python Abstraction for PyOrigin
PyOriginTools has Workbook, Worksheet, and Graph classes to provide a single layer of abstraction over the complicated (and often inconsistent) Origin object model which aims to make most Origin tasks single-line python solutions. Data is _always_ provided in native python and numpy data types (lists and dictionaries) and never obscure classes custom datatypes.

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
import PyOriginTools as OR # <-- this module is what you're reading about!
sheet=OR.Sheet()
print(sheet.colNames)
print(sheet.data)
```

For more, check out the section on [API design](documentation/API-design)

## PyOrigin.py Documentation
This module comes with an automatically generated HTML outline of PyOrigin.py functions, objects, and their properties. It also comes with inspection reports of common PyOrigin output objects (worksheetPages, worksheetPage, Column, etc.) generated with webinspect. Most of what is generated with these tools is available on http://swharden.com/software/pyorigin/

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

**Code and output are formatted nicely here:**

http://swharden.com/software/pyorigin/PyOrigin-examples.html

## Work with Origin Data _outside_ of Origin!
This package provides `SHEET` and `BOOK` classes that make it easy to wrap everything about a worksheet or workbook up in a single object which can be saved (as a pickle) to the disk. Now you can save a workbook or a worksheet from Origin, and play with its data outside Origin. There is even a HTML worksheet viewer which renders `SHEET` objects just as they would be seen in Origin!

**In an Origin session, we can save a worksheet to a file:**
```python
sheet=OR.SHEET() # pulls the active workbook/worksheet
OR.pickle_save(sheet,"demoSheet.pkl")
```

**Now we can load it in any console or IDE, such as Spyder:**
```python
sheet=OR.pickle_load("demoSheet.pkl")
sheet.colAdd(desc="demoCol",data=np.arange(15)**2)
sheet.viewHTML()
```
**The output of `viewHTML()` automatically loads in your browser:**
![](documentation/screenshots/fauxrigin.png)

## Useful Links
* http://swharden.com/software/pyorigin/
