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

## Inspecting workbooks

## Getting data from worksheets

## Create new worksheets before workbooks
To create something from scratch, we could do one of two things:
 1. create an empty book, create sheets, and add sheets into that book
 2. create sheets, add those sheets into a book
 
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
demoBook.addSheet(sheet3) # demonstrate how to add a sheet
demoBook.moveSheet(-1,0) # move the last sheet to the first spot

demoBook.transferToOrigin(overwrite=True) # communicates with PyOrigin to create/fill this book.
```
