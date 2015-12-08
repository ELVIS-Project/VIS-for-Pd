# -*- coding: UTF-8 -*-

"""
# ----- vis-vertical-intervals.py ------------------------------------ #

Symbolic music score parsing with music21, and indexing of the score 
into a pandas DataFrame via the NoteRestIndexer of the VIS-Framework. 
Once the DataFrame has been created all vertical intervals are 
calculated between the parts.

Author:		Reiner Kramer	
Email:		reiner@music.org
Updated:	12.07.2015

# -------------------------------------------------------------------- #
"""

import sys, os
import music21
from vis.analyzers.indexers import noterest, interval
import multiprocessing as mp

test_file = ('/Users/reiner/Documents/MusicAnalyses/VIS-for-Pd/' + 
	'scores/symbolic/De-profundis-clamavi_Josquin-Des-Prez_file1.krn')

def find_intervals(selected_file):
	"""
	Takes an indexed score and finds the horizontal intervals.
	>>> find_intervals(test_file).head()
	Indexer interval.IntervalIndexer                              
	Parts                        0,1   0,2   0,3   1,2   1,3   2,3
	0                           Rest  Rest  Rest  Rest  Rest  Rest
	6                           Rest   NaN   NaN  Rest  Rest   NaN
	8                           Rest  Rest  Rest  Rest  Rest  Rest
	12                             8  Rest  Rest  Rest  Rest   NaN
	16                             5  Rest  Rest  Rest  Rest  Rest
	"""

	the_score = music21.converter.parse(str(selected_file))
	indexed_score = noterest.NoteRestIndexer(the_score).run()
	mmm = {'mp':False}
	the_intervals = interval.IntervalIndexer(indexed_score,mmm).run()

	# Small collection for test printing.
	print the_intervals.head().to_csv()

def main():
	"""
	Using main only for doctest.
	"""
	import doctest
	doctest.testmod()

if __name__ == '__main__':
	main()

# ----- END vis-vertical-intervals.py -------------------------------- #