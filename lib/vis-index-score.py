# -*- coding: UTF-8 -*-

"""
# ----- vis-index-score.py ------------------------------------------- #

Symbolic music score parsing with music21, and indexing of the score 
into a pandas DataFrame via the NoteRestIndexer of the VIS-Framework.

Author:		Reiner Kramer	
Email:		reiner@music.org
Updated:	12.08.2015

# -------------------------------------------------------------------- #
"""

import sys, os, music21
from vis.analyzers.indexers import noterest

# Pd window message that music21 module has properly loaded.
try:
	print("{} loaded.".format(sys.argv))
except:
	print 

# Test file for running doctest.
test_file = ('../scores/symbolic/' + 
	'De-profundis-clamavi_Josquin-Des-Prez_file1.krn')

'''
test_file = ('/Users/reiner/Documents/MusicAnalyses/VIS-for-Pd/scores/symbolic/' + 
	'De-profundis-clamavi_Josquin-Des-Prez_file1.krn')
'''

def index_score(*args):
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
	parsed_score = music21.converter.parseFile(str(args[0]))
	indexed_score = noterest.NoteRestIndexer(parsed_score).run()

	if(str(args[2]) == 'end'):
		print '\n' + indexed_score.tail(args[1]).to_string(col_space=10)

	else:
		print '\n' + indexed_score.head(args[1]).to_string(col_space=10)


def main():
	'''
	Using main only for doctest.
	'''
	import doctest
	doctest.testmod()

if __name__ == '__main__':
	main()
 
 # ----- END vis-index-score.py -------------------------------------- #