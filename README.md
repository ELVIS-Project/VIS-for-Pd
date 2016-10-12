# VIS for Pd
VIS for Pd is a dataflow programming extension for the VIS-Framework, based on PureData (Pd).

![VIS-for-Pd Screenshot](https://cdn.rawgit.com/ELVIS-Project/VIS-for-Pd/master/images/VIS-for-Pd-New-Release.svg)

####Requirements
- Miller Puckette's [Pd-0.46-7](http://msp.ucsd.edu/software.html]).
  - It is highly recommended to work through a tutorial on how to use Pd first, before going any further. Johannes Kreidler wrote an excellent [Pd tutorial](http://www.pd-tutorial.com).
- Thomas Grill's [py/pyext](http://grrrr.org/research/software/py/). Follow the instructions on Grill's [py/pyext – Python scripting objects for Pure Data and Max](http://grrrr.org/research/software/py/) page, including where to add the binaries into the Pd environment. As a courtesy the py external binaries for Pd (Windows, Linux, and OSX) have bin included in the /lib/pre-compiled-externals folder. Use at your own risk, they may or may not work. 
- [Gem](https://github.com/umlaeute/Gem) by [umlaeute](https://github.com/umlaeute). Gem is used for visualization. Install this Pd external with [deken](https://github.com/pure-data/deken).
- Python, and the following modules:
  - Michael Cuthbert's [music21](https://github.com/cuthbertLab/music21). [Read the documentation](http://web.mit.edu/music21/doc/about/what.html).
  - McGill's [VIS-Framework](https://github.com/ELVIS-Project/vis-framework) developed by the [SIMSSA](https://simssa.ca) project. [Read the documentation](http://vis-framework.readthedocs.org/en/latest/).
  - The open source [pandas](https://github.com/pydata/pandas) library. [Read the documentation](http://pandas.pydata.org/pandas-docs/stable/10min.html).
