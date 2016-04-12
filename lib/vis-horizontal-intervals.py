# -*- coding: UTF-8 -*-

"""
# ----- vis-horizontal-intervals.py ---------------------------------- #

Symbolic music score parsing with music21, and indexing of the score 
into a pandas DataFrame via the NoteRestIndexer of the VIS-Framework.
Once the DataFrame has been created all horizontal intervals are 
calculated within a part.

Author:		Reiner Kramer	
Email:		reiner@music.org
Updated:	04.12.2016

# -------------------------------------------------------------------- #
"""

import sys, os
import music21
from vis.analyzers.indexers import noterest, interval

test_file = ('/Users/reiner/Documents/MusicAnalyses/VIS-for-Pd/' + 
	'scores/symbolic/De-profundis-clamavi_Josquin-Des-Prez_file1.krn')

'''
def index_score(symbolic_file):
	"""
	Indexes a symbolic music file.
	"""
	the_score = music21.converter.parse(str(symbolic_file))
	indexed_score = noterest.NoteRestIndexer(the_score).run()

	return indexed_score
'''

def find_intervals(symbolic_file):
	"""
	Takes an indexed score and finds the horizontal intervals.
	>>> find_intervals(test_file).head()
	Indexer interval.HorizontalIntervalIndexer                
	Parts                                    0   1     2     3
	0                                     Rest   1  Rest  Rest
	6                                      NaN   1   NaN   NaN
	8                                     Rest  -5  Rest  Rest
	12                                       1   4   NaN   NaN
	16                                     NaN  -2  Rest  Rest
	"""
	the_score = music21.converter.parse(str(symbolic_file))
	indexed_score = noterest.NoteRestIndexer(the_score).run()
	mmm = {'mp':False}
	the_intervals = interval.HorizontalIntervalIndexer(indexed_score,mmm).run()

	print the_intervals.head().to_csv()

#the_score = index_score(test_file)
#the_intervals = find_intervals(the_score)

def main():
	"""
	Using main only for doctest.
	"""

	import doctest
	doctest.testmod()

if __name__ == '__main__':
	main()

# ----- END vis-horizontal-intervals.py ------------------------------ #