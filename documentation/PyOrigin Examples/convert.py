"""
This script will generate a nice markdown-formatted
readme file by comparing source code with Orign output.

Inside origin, run the command:
    run -pyf "C:\path\to\examples.py" runall
    
Then save the command window output as output.txt

Now run this script, and README.md will be created.
(Actually, output.md will be created and combined with
readme_top.md to yield README.md)
"""

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
    out=open("readme_top.md").read()
    for title in sorted(code.keys()):
        out+='## {}() ##\n'.format(title.split("_",2)[-1])
        out+='**Python:**'
        out+="\n```python\n"+code[title]+"\n```\n"
        out+='**OriginLab Output:**'
        out+="\n```\n"+output[title]+"\n```\n"
    with open('README.md','w') as f:
        f.write(out)
    print(out)
    print("DONE")