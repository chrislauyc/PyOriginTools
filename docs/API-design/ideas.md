# Concepts

## referring to stuff
What is the difference between a workbook and a worksheet? I still can't figure it out, because what I call call workbooks are actually worksheet objects, and what I call worksheets are actually worksheetpage objects. Let's simplify the terms we use to refer to relevant Origin things.

|What I call|you can call a|but PyOrigin Calls it a|
|---|---|---|
|workbook|PyOriginTools.Book|CPyOriginCollectionPages|
|worksheet|PyOriginTools.Sheet|CPyWorksheetPage|
|graph|PyOriginTools.Graph|CPyGraphPage|
|name|name|short name|
|description|description|long name|
|folder|_object_.folder|folder|
|path|_object_.path|_object_.GetParent().GetFolder()|

## Importing PyOrigin and/or PyOriginTools
PyOriginTools is intended to serve as a logical, consistent, and well-documented layer between you and PyOrigin. Optimally you will never need to import PyOrigin and interact with it directly. If you do with to do this, you can always import PyOrigin and PyOriginTools in the same script and use your favorite features of each. 

To save keystrokes, I import PyOriginTools as OR:
```python
import PyOrigin # just in case we want to use it
import PyOriginTools as OR # abbreviation for Origin
```

# Organization
## High Level Operations
### Figuring out what our project contains
```python
print(OR.things()) # returns the names of everything (workbooks, graphs, notes)
print(OR.books()) # return the names of all workbooks
print(OR.graphs()) # return the names of all workbooks
print(OR.notes()) # return the names of all notes
```
