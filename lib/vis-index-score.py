# -*- coding: UTF-8 -*-
#!/usr/local/bin/python

"""
# ----- vis-index-score.py --------------------------------------------- #

Author:		Reiner Kramer	
Email:		reiner@music.org
Updated:	11.24.2015

Symbolic music score parsing with music21.

# -------------------------------------------------------------------- #
"""

import sys, os
import music21
from vis.analyzers.indexers import noterest

# Pd window message that file has properly loaded.
print("{} loaded.".format(os.path.basename(__file__)))
print("Using Python {}.{}.{}.".format(sys.version_info[0],
	sys.version_info[1],sys.version_info[2]))

# Pd window message that music21 module has properly loaded.
try:
	print("{} loaded via {}.".format(music21, sys.argv))
except:
	print 

def parse_score(selected_file):
	'''
	Uses the noterest indexer from the VIS-Framework to place a score 
	into a pandas DataFrame.
	'''

	the_score = music21.converter.parse(str(selected_file))
	indexed_score = noterest.NoteRestIndexer(the_score).run()

	# Returning the first measures only for now:
	return the_score.parts[1].measure(1).show('text')


def main():
	"""
	Using main only for doctest.
	"""
	import doctest
	doctest.testmod()

if __name__ == '__main__':
	main()
 


