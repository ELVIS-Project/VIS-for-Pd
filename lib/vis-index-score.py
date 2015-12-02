# -*- coding: UTF-8 -*-

"""
# ----- vis-index-score.py ------------------------------------------- #

Symbolic music score parsing with music21, and indexing of the score 
into a pandas DataFrame via the NoteRestIndexer of the VIS-Framework.

Author:		Reiner Kramer	
Email:		reiner@music.org
Updated:	12.02.2015

# -------------------------------------------------------------------- #
"""

import sys, os
import music21
from vis.analyzers.indexers import noterest

# Pd window message that music21 module has properly loaded.
try:
	print("{} loaded.".format(sys.argv))
except:
	print 

# A test file for running a doctest.

test_file = ('../scores/symbolic/' + 
	'De-profundis-clamavi_Josquin-Des-Prez_file1.krn')

def index_score(selected_file):
	'''
	Uses the noterest indexer from the VIS-Framework to place a score 
	into a pandas DataFrame.
	>>> index_score(test_file)
	Indexer noterest.NoteRestIndexer                
	Parts                          0   1     2     3
	0                           Rest  D4  Rest  Rest
	6                            NaN  D4   NaN   NaN
	8                           Rest  D4  Rest  Rest
	12                            G4  G3   NaN   NaN
	16                           NaN  C4  Rest  Rest
	'''

	the_score = music21.converter.parse(str(selected_file))
	indexed_score = noterest.NoteRestIndexer(the_score).run()

	print indexed_score.head()

def main():
	"""
	Using main only for doctest.
	"""
	import doctest
	doctest.testmod()

if __name__ == '__main__':
	main()
 
 # ----- END vis-index-score.py -------------------------------------- #