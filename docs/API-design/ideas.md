# Concepts

## referring to stuff
What is the difference between a workbook and a worksheet? I still can't figure it out, because what I call call workbooks are actually worksheet objects, and what I call worksheets are actually worksheetpage objects. Let's simplify the terms we use to refer to relevant Origin things.

|What I call|you can call a|but PyOrigin Calls it a|
|---|---|---|
|workbook|PyOriginTools.Book|OriginCollectionPages|
|worksheet|PyOriginTools.Sheet|WorksheetPage|
|graph|PyOriginTools.Graph|GraphPage|
|name|name|ShortName|
|description|description|LongName|
|folder|_object_.folder|Folder|
|path|_object_.path|_object_.GetParent().GetFolder()|

## Importing PyOrigin and/or PyOriginTools
PyOriginTools is intended to serve as a logical, consistent, and well-documented layer between you and PyOrigin. Optimally you will never need to import PyOrigin and interact with it directly. If you do with to do this, you can always import PyOrigin and PyOriginTools in the same script and use your favorite features of each. 

To save keystrokes, I import PyOriginTools as OR:
```python
import PyOrigin # just in case we want to use it
import PyOriginTools as OR # abbreviation for Origin
import numpy as np # because I use this all the time
```

# Organization
## High Level Operations
### Figuring out what our project contains
```python
OR.things() # returns the names of everything (workbooks, graphs, notes)
OR.books() # return the names of all workbooks
OR.graphs() # return the names of all workbooks
OR.notes() # return the names of all notes
```

# Pulling data from Origin
Most of what we are trying to do is read data from worksheets. We can acquire data directly from a worksheet (or workbook of worksheets), or by pulling in an entire workbook. In both cases, we can pull in either the active workbook/worksheet, or one defined by name.

## Pulling a single worksheet
This is almost identical, except we can assign a sheet directly by bookName/sheetName:
```python
demoSheet=OR.Sheet("FruityBook","Sheet1") # pull a sheet by its bookName/sheetName
print('The first sheet "{}" has {} sheets').format(demoSheet.name,len(demoSheet.cols))
print(demoSheet.cols) # prints the names of every column in the sheet
print(demoSheet.data) # this prints the numpy array of all data contained within
```

## Pulling a whole workbook
```python
demoBook=OR.Book("FruityBook",pull=True) # if we didn't set pull as True, we would be creating one from scratch
print('The book "{}" has {} sheets').format(demoBook.name,len(demoBook.sheets))
firstSheet=demoBook.sheets[0] # let's look at the first sheet in the workbook
print('The first sheet "{}" has {} sheets').format(firstSheet.name,len(firstSheet.cols))
print(firstSheet.name,"has",len(demoBook.sheets),"sheets")
print(firstSheet.cols) # prints the names of every column in the sheet
print(firstSheet.data) # this prints the numpy array of all data contained within
```

## Modifying a worksheet and pushing it back to Origin
```python
demoSheet=OR.Sheet("FruityBook","Sheet1") # pull a sheet by its bookName/sheetName
demoSheet.data[2,3]=1234 # set the value of a cell (row 2, column 3)
demoSheet.transferToOrigin("FruityBook","Sheet1",overwrite=True) # to push it back into Origin
```

## Modifying a workbook and pushing it back to Origin
```python
demoBook=OR.Book("FruityBook",pull=True) # if we didn't set pull as True, we would be creating one from scratch
demoBook.sheets[0].data[2,3]=1234 # from the first sheet, set the value of a cell (row 2, column 3)
demoBook.addSheet("blankSheet") # let's add a new sheet to the end of the workbook
demobook.sheets[-1].cols=["some","new","data","columns"] # make the new (last) sheet interesting
demoBook.transferToOrigin("FruityBook",overwrite=True) # to push it back into Origin overwriting the original
```

# Pushing data to Origin

## Create new worksheets before workbooks
To create something from scratch, we could do one of two things:
 1. create an empty book, create sheets, and add sheets into that book, then push to Origin
 2. create sheets, add those sheets into a book, then push to Origin
 
Although it feels backwards, #2 seems simpler, so I'm going to go with it. In general, create a sheet before you determine what book to insert it into (including a book which may need to be created)

## Creating worksheets and workbooks from scratch
In this demo we will create a worksheet with some fruity data, then create several similar worksheets from this same staring point, and push it all into a workbook ("fruityBook") in Origin. Note that all of this occurs in Python memory until the very last line, when it interacts with Origin
```python
# this line shows how to initiate a worksheet with everything we need in one line
sheet1=OR.Sheet("sheet1",cols=["time","apples","oranges","pears"],units=["seconds","grams","grams","grams"])
sheet1.data=np.random.random_sample((10,3))*10 # random values (10 rows, 3 columns)

# we can copy the sheet so we can mess around with it
sheet2=copy(sheet1) # remember that without copy() we would be messing with the original
sheet2.name="sheet2"
sheet2.units[0]="minutes"
sheet2.cols[1]="granny smith"
sheet2.data=np.sqrt(sheet2.data)
sheet2.comments=["comment one","comment two","comment three"]
sheet2.data=sheet2.data*1000

# let's make sheet3 nothing but values '123'
sheet3=copy(sheet1)
sheet3.name="sheet3"
sheet3.units=None # untits will be blank
sheet3.comments=None # comments will be blank
sheet3.cols=[x.upper() for x in sheet3.cols] # make every name uppercase
sheet3.data=np.round(np.sqrt(sheet3.data),1) # round the sqrt to 1 decimal place
sheet3.data[3,2]=None # make a single cell of sheet 3 empty

# now it's time to create our workbook!
demoBook=OR.Book("FruityBook",sheets=[sheet1, sheet2]) # initiate with 2 sheets
demoBook.


(sheet3) # demonstrate how to add a sheet
demoBook.moveSheet(-1,0) # move the last sheet to the first spot

demoBook.transferToOrigin(overwrite=True) # communicates with PyOrigin to create/fill this book.
```
