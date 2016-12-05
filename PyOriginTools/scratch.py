"""
scratch pad for functin ideas.
DONT LET THINGS SIT IN HERE FOR LONG!
"""

# PREPARE TO IMPORT INTELLIGENTLY
import os
import sys
if not "../" in sys.path:
    sys.path.append('../') # this helps my IDE be happy
newpath=os.path.abspath(os.path.dirname(os.path.dirname(sys.argv[0])))
if not newpath in sys.path:
    sys.path.append(newpath) # this is really where it's at

# DO THE IMPORTS
import PyOriginTools
import PyOrigin # this is my sham one in my IDE
import webinspect

if __name__=="__main__":
    print("DO NOT RUN THIS SCRIPT DIRECTLY.")
    print("Version",PyOriginTools.__version__)