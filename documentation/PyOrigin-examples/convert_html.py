"""
This script will generate a nice HTML demo file
by comparing source code with Orign output.

Inside origin, run the command:
    run -pyf "C:\path\to\examples.py" runall
    
Then save the command window output as output.txt

Now run this script to make PyOrigin-examples.html
"""

TEMPLATE=open("template.html").read().split("\n")

def getCodeBlocks():
    """return a dict with the code for each function"""
    raw=open("examples.py").read()
    d={}
    for block in raw.split("if __name__")[0].split("\ndef "):
        title=block.split("\n")[0].split("(")[0]
        if not title.startswith("demo_"):
            continue
        code=[x[4:] for x in block.split("\n")[1:] if x.startswith("    ")]
        d[title]="\n".join(code).strip()
    return d
        
def getOutputBlocks():
    """return a dict with the output of each function"""
    raw=open("output.txt").read()
    d={}
    for block in raw.split("\n####### ")[1:]:
        title=block.split("\n")[0].split("(")[0]
        block=block.split("\n",1)[1].strip()
        d[title]=block.split("\nfinished in ")[0]
    return d

if __name__=="__main__":
    code=getCodeBlocks()
    output=getOutputBlocks()
    out=TEMPLATE[0]
    for title in sorted(code.keys()):
        out+='<div class="block">%s()</div>'%title.split("_",2)[-1]
        out+='<div style="margin-left: 20px;">'
        out+=TEMPLATE[1].replace("CODE",code[title])
        out+=TEMPLATE[2].replace("CODE",output[title])
        out+='</div>'
    with open('PyOrigin-examples.html','w') as f:
        f.write(out+TEMPLATE[3])
    print("DONE")