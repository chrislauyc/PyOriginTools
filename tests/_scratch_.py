import sys
import os
sys.path.insert(0,"../")

import PyOriginTools as OR
import numpy as np

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
    sheet=OR.pickle_load(R"C:\Users\swharden\1481408002.pkl")
    while(sheet.nCols>10):
        sheet.colDelete()
    sheet.colAdd(desc="demoCol",data=np.arange(15)**2)
    sheetToHTML(sheet)
    print("DONE")