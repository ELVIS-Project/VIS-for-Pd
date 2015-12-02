# -*- coding: UTF-8 -*-
#!/usr/local/bin/python

"""
# ----- bang-test.py ------------------------------------------------- #

Author:		Reiner Kramer	
Email:		reiner@music.org
Updated:	11.24.2015

Filtering a bang ...

# -------------------------------------------------------------------- #
"""

import sys, os
import music21

# Pd window message that file has properly loaded.
print("{} loaded.".format(os.path.basename(__file__)))
print("Using Python {}.{}.{}.".format(sys.version_info[0],
	sys.version_info[1],sys.version_info[2]))

# Pd window message that music21 module has properly loaded.
try:
	print("{} loaded via {}.".format(music21, sys.argv))
except:
	print 

def bang_filter(something):
	"""
	Filters a bang message.
	"""
	if(str(something) == 'bang'):
		message = ('Bang {0} {0}!'.format(str(something)))
	else:
		message = ('No {0}.'.format(str(something)))

	return message


