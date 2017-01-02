# Columns with many NANNUM cells crash GetData() 
This bug causes Origin to have a HARD CRASH whenever PyOrigin's GetData() is called from a column which has NANNUM values. It crashes around 3,000 reads and seems to be cumulative across python scripts.

## Recreating the Issue
**1.) In a fresh Origin, create a worksheet with a lot of data:**
```python
sheetObject=PyOrigin.ActiveLayer()
sheetObject.Columns(1).SetData(range(10000),0)
```

**2.) manually put data into the first column**
* copy/paste data from the second column into the first column
* if left alone, the next step will never crash Origin
* if the first column is highlighted and "delete" pressed, the next step will crash Origin

**3.) read the data 100 times (may die on read #3)**
```python
for i in range(100):
    PyOrigin.LT_execute("type Columns(0).GetData() attempt %s;"%(i))
    sheetObject.Columns(0).GetData()
```

## hack-in solving the issue
It seems that blank cells are what kills Origin. Running this once before GetData() is called solves this problem.
```python
PyOrigin.LT_execute('wreplace find_value:="--" replace_str:=""')
```
