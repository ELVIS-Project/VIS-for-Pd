# -*- coding: UTF-8 -*-

"""
# ----- vis-ngram.py ------------------------------------------------- #

Symbolic music score parsing with music21, and indexing of the score 
into a pandas DataFrame via the NoteRestIndexer of the VIS-Framework.
Once the DataFrame has been created and all horizontal and vertical 
intervals have been placed into seperate DataFrames, a new N-gram 
DataFrame can be created.

Author:		Reiner Kramer	
Email:		reiner@music.org
Updated:	12.03.2015

# -------------------------------------------------------------------- #
"""

import sys, os
import music21
from vis.analyzers.indexers import noterest, interval

def index_score(symbolic_file):
	"""
	Indexes a symbolic music file.
	"""
	mto_score = music21.converter.parse(str(symbolic_file))
	df_score = noterest.NoteRestIndexer(mto_score).run()

	return df_score

def hor_intervals(df_score):
	"""
	Creates a set of horizontal intervals according to passed in 
	specifications.
	"""

	settings = {'mp':False}
	h_ints = interval.HorizontalIntervalIndexer(df_score,settings).run()

	return h_ints

def ver_intervals(df_score):
	"""
	Creates a set of vertical intervals according to passed in 
	specifications.
	"""

	settings = {'mp':False}
	v_ints = interval.IntervalIndexer(df_score, settings).run()

	return v_ints


# ----- END vis-ngram.py --------------------------------------------- #