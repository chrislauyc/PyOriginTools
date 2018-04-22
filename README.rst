PyOriginTools
==============

PyOriginTools is a collection of scripts and examples intended to make life easier for those who want to develop python scripts which interact with OriginLab (and software written in OriginC) using Origin's embedded Python environment using their PyOrigin module. Because the PyOrigin.py that ships with Origin is automatically generated using SWIG (http://www.swig.org/Doc1.3/Python.html), it is structured a C program (not very pythonic) and cannot be learned intuitively because it is devoid of intrinsic documentation (docstrings) which guide the programmer at the time of coding. The Official Origin/Python documentation (http://www.originlab.com/doc/python/PyOrigin) is a good start, but not suffecient to learn this object model for those not already familiar with it.

This module is intended to be installed in a python distribution which lives somewhere Origin can see it. It utilizes tools such as numerical analysis tools such as numpy which do not ship with OriginLab.

WARNING: ABANDONWARE!
---------------------

Although a lot of effort was initially invested in this project, I decided just to perform all data analysis for my own needs in pure Python. PyOriginTools relies somewhat on SWHLab which I have since replaced with pyABF. I have stopped maintaining PyOriginTools (which tends to break as new Origin versions are released), and am leaving it up to the core OriginLab developers to improve Python support (and documentation) to the point where it's intuitive and functional. Code has been left here intact for backup and educational purposes.

GitHub Project
---------------------
https://github.com/swharden/PyOriginTools