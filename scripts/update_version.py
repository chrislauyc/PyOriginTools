import os

def updateVersion(fname):
    """
    given a filename to a file containing a __counter__ variable,
    open it, read the count, add one, rewrite the file.

    This:
        __counter__=123
    Becomes:
        __counter__=124

    """
    fname=os.path.abspath(fname)
    if not os.path.exists(fname):
        print("can not update version! file doesn't exist:\n",fname)
        return
    with open(fname) as f:
        raw=f.read().split("\n")
    for i,line in enumerate(raw):
        if line.startswith("__counter__="):
            version=int(line.split("=")[1])
            raw[i]="__counter__=%d"%(version+1)
    with open(fname,'w') as f:
        f.write("\n".join(raw))
    print("upgraded version %d -> %d"%(version,version+1))

if __name__=='__main__':
    updateVersion('../PyOriginTools/version.py')