# PyOrigin Examples
A demonstration of how I perform some of the most common tasks using PyOrigin. This readme file generated automatically by running all of the tests in [examples.py](examples.py), saving its output as [output.txt](output.txt), and generating this markdown-formatted summary page thanks to [convert.py](convert.py)

## showPaths() ##
**Python:**
```python
print("This is where Origin is looking when 'import' statements are used:")
print("\n".join(sys.path))
return
```
**OriginLab Output:**
```
This is where Origin is looking when 'import' statements are used:
C:\Users\swharden\Documents\GitHub\python-OriginLab\originlab
C:\Program Files\OriginLab\Origin2017\64bit\PyDLLs
C:\Program Files\OriginLab\Origin2017\python35.zip
C:\Program Files\OriginLab\Origin2017\64bit\PyDLLs\python35.zip
C:\Program Files\Python35\Lib
C:\Program Files\Python35\DLLs
C:\Program Files\OriginLab\Origin2017
C:\Program Files\Python35\Lib\site-packages
```
## createBook() ##
**Python:**
```python
print("starting by destroyold and old 'SWHdemo' books...")
PyOrigin.DestroyPage('SWHdemo')
print("now creating a 'SWHdemo' book from scratch...")
worksheetPage=PyOrigin.CreatePage(2,"","Origin",1) # 2 means worksheet, 1 means not hidden
print("short name was:",worksheetPage.GetName()) # automatically assigned
worksheetPage.SetName("SWHdemo")
print("short name is now:",worksheetPage.GetName()) # must be unique
worksheetPage.SetLongName("fancy pancy empty workbook") # doesn't have to be unique
print("number of sheets:",worksheetPage.Layers().GetCount()) # 1 sheet = 1 layer?
```
**OriginLab Output:**
```
starting by destroyold and old 'SWHdemo' books...
now creating a 'SWHdemo' book from scratch...
short name was: Book2
short name is now: SWHdemo
number of sheets: 1
```
## addSheet() ##
**Python:**
```python
page=PyOrigin.Pages('SWHdemo')
sheet=page.AddLayer('SheetDemo') # creates sheet and returns it
bookName,sheetName,sheetIndex=sheet.GetPage().GetName(),sheet.GetName(),sheet.GetIndex()
print('created [{}]{} (index {})'.format(bookName,sheetName,sheetIndex))
sheet.SetIndex(0) # moves this sheet to the front
```
**OriginLab Output:**
```
created [SWHdemo]SheetDemo (index 1)
```
## populateSheet() ##
**Python:**
```python
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
```
**OriginLab Output:**
```
number of columns before: 2
  adding a column: "SWH" at position 1...
  adding a column: "SWH" at position 1...
  adding a column: "SWH" at position 1...
  adding a column: "SWH" at position 1...
  adding a column: "SWH" at position 1...
  adding a column: "SWH" at position 1...
  adding a column: "SWH" at position 1...
  adding a column: "SWH" at position 1...
  adding a column: "SWH" at position 1...
  adding a column: "SWH" at position 1...
number of columns now: 12
  deleting column 1...
  deleting column 1...
  deleting column 1...
  deleting column 1...
  deleting column 1...
deleting all but 5 rows one by one...
number of columns now: 7
  filling column 0 with [  0.19   1.21   2.18   3.31   4.57   5.81   6.81   7.84   8.11   9.64
  10.52  11.24  12.59  13.38  14.25  15.27  16.14  17.05  18.25  19.18
  20.25  21.57  22.53  23.45  24.27  25.63  26.52  27.01  28.61  29.3   30.9
  31.56  32.6   33.53  34.18  35.83  36.64  37.47  38.31  39.36  40.69
  41.85  42.91  43.53  44.68  45.03  46.52  47.91  48.02  49.41]
  filling column 1 with [  0.68   2.31   4.47   6.25   8.39  10.69  12.29  14.9   16.59  18.96
  20.42  22.66  24.13  27.    28.18  30.43  32.49  34.6   36.6   38.5
  40.57  42.14  44.22  46.18  48.21  50.67  52.11  54.33  56.71  58.31
  60.99  62.41  64.17  66.7   68.24  70.58  72.8   74.26  76.21  78.44
  80.54  82.69  85.    86.99  88.39  90.76  92.85  94.52  96.45  98.79]
  filling column 2 with [   0.94    3.45    6.26    9.97   12.43   15.18   18.79   21.59   24.46
   27.49   30.51   33.27   36.07   39.72   42.2    45.02   48.41   51.72
   54.22   57.7    60.9    63.04   66.68   69.52   72.63   75.15   78.01
   81.11   84.8    87.01   90.52   93.16   96.54   99.3   102.93  105.01
  108.53  111.07  114.98  117.61  120.5   123.77  126.06  129.65  132.96
  135.64  138.62  141.59  144.34  147.06]
  filling column 3 with [   0.61    4.29    8.84   12.37   16.02   20.27   24.98   28.08   32.46
   36.96   40.22   44.6    48.77   52.56   56.92   60.6    64.46   68.87
   72.76   76.09   80.71   84.87   88.15   92.56   96.61  100.5   104.36
  108.26  112.7   116.22  120.03  124.11  128.07  132.69  136.22  140.77
  144.67  148.78  152.83  156.8   160.3   164.14  168.02  172.78  176.85
  180.8   184.58  188.78  192.21  196.75]
  filling column 4 with [   0.27    5.82   10.08   15.24   20.96   25.91   30.2    35.29   40.85
   45.37   50.06   55.71   60.6    65.54   70.6    75.3    80.43   85.71
   90.55   95.39  100.24  105.23  110.26  115.46  120.85  125.22  130.94
  135.51  140.23  145.58  150.26  155.59  160.45  165.23  170.69  175.1
  180.73  185.43  190.83  195.9   200.53  205.73  210.17  215.91  220.61
  226.    230.59  235.43  240.19  245.53]
  filling column 5 with [   0.7     6.87   12.83   18.1    24.64   30.33   36.91   42.39   48.71
   54.73   60.07   66.29   72.56   78.23   84.92   90.13   96.56  102.98
  108.8   114.98  120.8   126.92  132.42  138.9   144.44  150.96  156.34
  162.18  168.14  174.98  180.65  186.59  192.05  198.04  204.53  210.55
  216.47  222.85  228.34  234.89  240.56  246.27  252.1   258.35  264.07
  270.85  276.46  282.26  288.39  294.09]
  filling column 6 with [  3.30000000e-01   7.78000000e+00   1.47000000e+01   2.14700000e+01
   2.81200000e+01   3.58300000e+01   4.20700000e+01   4.96500000e+01
   5.61100000e+01   6.36500000e+01   7.08400000e+01   7.70500000e+01
   8.46100000e+01   9.10600000e+01   9.84900000e+01   1.05780000e+02
   1.12910000e+02   1.19710000e+02   1.26470000e+02   1.33060000e+02
   1.40850000e+02   1.47610000e+02   1.54320000e+02   1.61550000e+02
   1.68440000e+02   1.76000000e+02   1.82150000e+02   1.89730000e+02
   1.96240000e+02   2.03370000e+02   2.10450000e+02   2.17350000e+02
   2.24810000e+02   2.31600000e+02   2.38940000e+02   2.45310000e+02
   2.52890000e+02   2.60000000e+02   2.66090000e+02   2.73170000e+02
   2.80060000e+02   2.87060000e+02   2.94780000e+02   3.01860000e+02
   3.08430000e+02   3.15390000e+02   3.22410000e+02   3.29600000e+02
   3.36360000e+02   3.43390000e+02]
deleting row 10
deleting row 11
deleting row 12
deleting row 13
deleting row 14
```
## inspect_workbooks() ##
**Python:**
```python
print("gives details for all workbooks in the project")
print("Worksheet Pages:")
print("\n".join(["  "+page.GetName() for page in PyOrigin.WorksheetPages()]))
```
**OriginLab Output:**
```
gives details for all workbooks in the project
Worksheet Pages:
  Book1
  SWHdemo
```
## inspect_graphs() ##
**Python:**
```python
print("gives details for all graphs in the project")
print("(there may not be any!)")
for page in PyOrigin.GraphPages():
    print(page.GetFolder(),page.GetName())
```
**OriginLab Output:**
```
gives details for all graphs in the project
(there may not be any!)
```
## inspect_pages() ##
**Python:**
```python
print("gives details for all pages (graphs and worksheets) in the project")
for page in PyOrigin.GraphPages():
    print("Type: {} Name: {}".format(page.GetType(),page.GetName()))
```
**OriginLab Output:**
```
gives details for all pages (graphs and worksheets) in the project
```
## list_pages() ##
**Python:**
```python
print("listing all pages (graphs and worksheets) in the project by their name")
pages_all=[x.GetName() for x in PyOrigin.Pages()]
pages_worksheets=[x.GetName() for x in PyOrigin.Pages() if x.GetType()==2]
pages_graph=[x.GetName() for x in PyOrigin.Pages() if x.GetType()==3]
print("PAGES:",pages_all)
print("WORKSHEETS:",pages_worksheets)
print("GRAPHS:",pages_graph)
```
**OriginLab Output:**
```
listing all pages (graphs and worksheets) in the project by their name
PAGES: ['Book1', 'SWHdemo']
WORKSHEETS: ['Book1', 'SWHdemo']
GRAPHS: []
```
## active() ##
**Python:**
```python
print("showing basics about what's active.")
print("PyOrigin.ActiveFolder():",PyOrigin.ActiveFolder())
print("PyOrigin.ActiveFolder().Path():",PyOrigin.ActiveFolder().Path())
print("PyOrigin.ActiveLayer():",PyOrigin.ActiveLayer())
try:
    print("PyOrigin.ActivePage():",PyOrigin.ActivePage())
except:
    print("PyOrigin.ActivePage(): CRASHED!!!! Does that when notes are selected.")
```
**OriginLab Output:**
```
showing basics about what's active.
PyOrigin.ActiveFolder(): Folder1
PyOrigin.ActiveFolder().Path(): /UNTITLED/Folder1/
PyOrigin.ActiveLayer(): SheetDemo
PyOrigin.ActivePage(): SWHdemo
```
## list_workbook_sheets() ##
**Python:**
```python
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
```
**OriginLab Output:**
```
selecting a worksheet page by its name
workbooks available (oldest to newest): ['Book1', 'SWHdemo']
selecting oldest workbook by its name: "Book1"
found 1 sheets:
PyOrigin.WorksheetPages("Book1").Layers(0) will select Sheet1 sheet
```
## active_worksheet_info() ##
**Python:**
```python
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
```
**OriginLab Output:**
```
showing info on the currently selected sheet of the active workbook
This page name is: SWHdemo
This page type is: 2
active book: "SWHdemo"
active sheet: "SheetDemo" (index: 0)
I see 7 columns with 45 rows
column short names: ['Scott0', 'Scott1', 'Scott2', 'Scott3', 'Scott4', 'Scott5', 'Scott6']
column long names: ['neuron 0', 'neuron 1', 'neuron 2', 'neuron 3', 'neuron 4', 'neuron 5', 'neuron 6']
column types: [X, Y, Y, Y, Y, Y, Y]
column data lengths: [45, 45, 45, 45, 45, 45, 45]
the last column contains data: [0.33, 7.78, 14.7, 21.47, 28.12, 35.83, 42.07, 49.65, 56.11, 63.65, 105.78, 112.91, 119.71, 126.47, 133.06, 140.85, 147.61, 154.32, 161.55, 168.44, 176.0, 182.15, 189.73, 196.24, 203.37, 210.45, 217.35, 224.81, 231.6, 238.94, 245.31, 252.89, 260.0, 266.09, 273.17, 280.06, 287.06, 294.78, 301.86, 308.43, 315.39, 322.41, 329.6, 336.36, 343.39]
```
## active_worksheet_data_numpy() ##
**Python:**
```python
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
```
**OriginLab Output:**
```
convertinng data of the selected worksheet to a 2D numpy array
WARNING: this may crash if you have letters in your document.


Fancy numpy array:
[[  1.90000000e-01   6.80000000e-01   9.40000000e-01   6.10000000e-01
    2.70000000e-01   7.00000000e-01   3.30000000e-01]
 [  1.21000000e+00   2.31000000e+00   3.45000000e+00   4.29000000e+00
    5.82000000e+00   6.87000000e+00   7.78000000e+00]
 [  2.18000000e+00   4.47000000e+00   6.26000000e+00   8.84000000e+00
    1.00800000e+01   1.28300000e+01   1.47000000e+01]
 [  3.31000000e+00   6.25000000e+00   9.97000000e+00   1.23700000e+01
    1.52400000e+01   1.81000000e+01   2.14700000e+01]
 [  4.57000000e+00   8.39000000e+00   1.24300000e+01   1.60200000e+01
    2.09600000e+01   2.46400000e+01   2.81200000e+01]
 [  5.81000000e+00   1.06900000e+01   1.51800000e+01   2.02700000e+01
    2.59100000e+01   3.03300000e+01   3.58300000e+01]
 [  6.81000000e+00   1.22900000e+01   1.87900000e+01   2.49800000e+01
    3.02000000e+01   3.69100000e+01   4.20700000e+01]
 [  7.84000000e+00   1.49000000e+01   2.15900000e+01   2.80800000e+01
    3.52900000e+01   4.23900000e+01   4.96500000e+01]
 [  8.11000000e+00   1.65900000e+01   2.44600000e+01   3.24600000e+01
    4.08500000e+01   4.87100000e+01   5.61100000e+01]
 [  9.64000000e+00   1.89600000e+01   2.74900000e+01   3.69600000e+01
    4.53700000e+01   5.47300000e+01   6.36500000e+01]
 [  1.52700000e+01   3.04300000e+01   4.50200000e+01   6.06000000e+01
    7.53000000e+01   9.01300000e+01   1.05780000e+02]
 [  1.61400000e+01   3.24900000e+01   4.84100000e+01   6.44600000e+01
    8.04300000e+01   9.65600000e+01   1.12910000e+02]
 [  1.70500000e+01   3.46000000e+01   5.17200000e+01   6.88700000e+01
    8.57100000e+01   1.02980000e+02   1.19710000e+02]
 [  1.82500000e+01   3.66000000e+01   5.42200000e+01   7.27600000e+01
    9.05500000e+01   1.08800000e+02   1.26470000e+02]
 [  1.91800000e+01   3.85000000e+01   5.77000000e+01   7.60900000e+01
    9.53900000e+01   1.14980000e+02   1.33060000e+02]
 [  2.02500000e+01   4.05700000e+01   6.09000000e+01   8.07100000e+01
    1.00240000e+02   1.20800000e+02   1.40850000e+02]
 [  2.15700000e+01   4.21400000e+01   6.30400000e+01   8.48700000e+01
    1.05230000e+02   1.26920000e+02   1.47610000e+02]
 [  2.25300000e+01   4.42200000e+01   6.66800000e+01   8.81500000e+01
    1.10260000e+02   1.32420000e+02   1.54320000e+02]
 [  2.34500000e+01   4.61800000e+01   6.95200000e+01   9.25600000e+01
    1.15460000e+02   1.38900000e+02   1.61550000e+02]
 [  2.42700000e+01   4.82100000e+01   7.26300000e+01   9.66100000e+01
    1.20850000e+02   1.44440000e+02   1.68440000e+02]
 [  2.56300000e+01   5.06700000e+01   7.51500000e+01   1.00500000e+02
    1.25220000e+02   1.50960000e+02   1.76000000e+02]
 [  2.65200000e+01   5.21100000e+01   7.80100000e+01   1.04360000e+02
    1.30940000e+02   1.56340000e+02   1.82150000e+02]
 [  2.70100000e+01   5.43300000e+01   8.11100000e+01   1.08260000e+02
    1.35510000e+02   1.62180000e+02   1.89730000e+02]
 [  2.86100000e+01   5.67100000e+01   8.48000000e+01   1.12700000e+02
    1.40230000e+02   1.68140000e+02   1.96240000e+02]
 [  2.93000000e+01   5.83100000e+01   8.70100000e+01   1.16220000e+02
    1.45580000e+02   1.74980000e+02   2.03370000e+02]
 [  3.09000000e+01   6.09900000e+01   9.05200000e+01   1.20030000e+02
    1.50260000e+02   1.80650000e+02   2.10450000e+02]
 [  3.15600000e+01   6.24100000e+01   9.31600000e+01   1.24110000e+02
    1.55590000e+02   1.86590000e+02   2.17350000e+02]
 [  3.26000000e+01   6.41700000e+01   9.65400000e+01   1.28070000e+02
    1.60450000e+02   1.92050000e+02   2.24810000e+02]
 [  3.35300000e+01   6.67000000e+01   9.93000000e+01   1.32690000e+02
    1.65230000e+02   1.98040000e+02   2.31600000e+02]
 [  3.41800000e+01   6.82400000e+01   1.02930000e+02   1.36220000e+02
    1.70690000e+02   2.04530000e+02   2.38940000e+02]
 [  3.58300000e+01   7.05800000e+01   1.05010000e+02   1.40770000e+02
    1.75100000e+02   2.10550000e+02   2.45310000e+02]
 [  3.66400000e+01   7.28000000e+01   1.08530000e+02   1.44670000e+02
    1.80730000e+02   2.16470000e+02   2.52890000e+02]
 [  3.74700000e+01   7.42600000e+01   1.11070000e+02   1.48780000e+02
    1.85430000e+02   2.22850000e+02   2.60000000e+02]
 [  3.83100000e+01   7.62100000e+01   1.14980000e+02   1.52830000e+02
    1.90830000e+02   2.28340000e+02   2.66090000e+02]
 [  3.93600000e+01   7.84400000e+01   1.17610000e+02   1.56800000e+02
    1.95900000e+02   2.34890000e+02   2.73170000e+02]
 [  4.06900000e+01   8.05400000e+01   1.20500000e+02   1.60300000e+02
    2.00530000e+02   2.40560000e+02   2.80060000e+02]
 [  4.18500000e+01   8.26900000e+01   1.23770000e+02   1.64140000e+02
    2.05730000e+02   2.46270000e+02   2.87060000e+02]
 [  4.29100000e+01   8.50000000e+01   1.26060000e+02   1.68020000e+02
    2.10170000e+02   2.52100000e+02   2.94780000e+02]
 [  4.35300000e+01   8.69900000e+01   1.29650000e+02   1.72780000e+02
    2.15910000e+02   2.58350000e+02   3.01860000e+02]
 [  4.46800000e+01   8.83900000e+01   1.32960000e+02   1.76850000e+02
    2.20610000e+02   2.64070000e+02   3.08430000e+02]
 [  4.50300000e+01   9.07600000e+01   1.35640000e+02   1.80800000e+02
    2.26000000e+02   2.70850000e+02   3.15390000e+02]
 [  4.65200000e+01   9.28500000e+01   1.38620000e+02   1.84580000e+02
    2.30590000e+02   2.76460000e+02   3.22410000e+02]
 [  4.79100000e+01   9.45200000e+01   1.41590000e+02   1.88780000e+02
    2.35430000e+02   2.82260000e+02   3.29600000e+02]
 [  4.80200000e+01   9.64500000e+01   1.44340000e+02   1.92210000e+02
    2.40190000e+02   2.88390000e+02   3.36360000e+02]
 [  4.94100000e+01   9.87900000e+01   1.47060000e+02   1.96750000e+02
    2.45530000e+02   2.94090000e+02   3.43390000e+02]]


Printing line by (x,y) coordinates (to row 5):
row: 0, col: 0, cell=0.19
row: 0, col: 1, cell=0.68
row: 0, col: 2, cell=0.94
row: 0, col: 3, cell=0.61
row: 0, col: 4, cell=0.27
row: 0, col: 5, cell=0.7
row: 0, col: 6, cell=0.33
row: 1, col: 0, cell=1.21
row: 1, col: 1, cell=2.31
row: 1, col: 2, cell=3.45
row: 1, col: 3, cell=4.29
row: 1, col: 4, cell=5.82
row: 1, col: 5, cell=6.87
row: 1, col: 6, cell=7.78
row: 2, col: 0, cell=2.18
row: 2, col: 1, cell=4.47
row: 2, col: 2, cell=6.26
row: 2, col: 3, cell=8.84
row: 2, col: 4, cell=10.08
row: 2, col: 5, cell=12.83
row: 2, col: 6, cell=14.7
row: 3, col: 0, cell=3.31
row: 3, col: 1, cell=6.25
row: 3, col: 2, cell=9.97
row: 3, col: 3, cell=12.37
row: 3, col: 4, cell=15.24
row: 3, col: 5, cell=18.1
row: 3, col: 6, cell=21.47
row: 4, col: 0, cell=4.57
row: 4, col: 1, cell=8.39
row: 4, col: 2, cell=12.43
row: 4, col: 3, cell=16.02
row: 4, col: 4, cell=20.96
row: 4, col: 5, cell=24.64
row: 4, col: 6, cell=28.12


Printing line by (x,y) coordinates (to row 5):
   0.19	   0.68	   0.94	   0.61	   0.27	   0.70	   0.33	
   1.21	   2.31	   3.45	   4.29	   5.82	   6.87	   7.78	
   2.18	   4.47	   6.26	   8.84	  10.08	  12.83	  14.70	
   3.31	   6.25	   9.97	  12.37	  15.24	  18.10	  21.47	
   4.57	   8.39	  12.43	  16.02	  20.96	  24.64	  28.12	
```
## redrawScreen() ##
**Python:**
```python
print("refreshing the Origin window")
#TODO: is there a PyOrigin way to do this?
PyOrigin.LT_execute("doc -uw;")
```
**OriginLab Output:**
```
refreshing the Origin window
```
