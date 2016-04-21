# -*- coding: utf-8 -*-
'''
# ----- Analysis.py -------------------------------------------------- #

Author: Reiner Kramer
Email:  reiner@music.org
Date:   12.10.2015

This is the main analysis script file used to create the Mode-Finder
program. The purpose is to create a set of algorithms that can be used 
to build a heuristic mode finding algorithm based on Glarean's 
Dodecachordon. The algorithm in turn can be used to analyze and group
period compositions (i.e. by composers mentioned by Glarean, and other
contemporary composers).

# -------------------------------------------------------------------- #
'''

# Import music21.
import music21

# Import pandas.
import pandas

# Import vis-framework items.
'''
# ----- working with pep installed vis ----- #
from vis.analyzers.indexers import noterest
from vis.analyzers.indexers import interval
from vis.analyzers.indexers import offset
'''
# ----- working with bleeding edge vis ----- #
from vis.analyzers.indexers import noterest
from vis.analyzers.indexers import interval
from vis.analyzers.indexers import offset
from vis.analyzers.indexers import ngram

# Import custom libraries.
# from lib import tester
# Testing the cutom library import.
# tester.make_it_so()

# ----- Parsing a score ---------------------------------------------- #

# Basis VIS-Workflow

# Path to score.

directory = ('/Users/reiner/Documents/MusicAnalyses/VIS-for-Pd/scores/')

symbolic_score = (directory + 'polyphonic/symbolic/' +
	'Book-3_Jacob-Obrecht_Monad_p-252_p-327.xml')

nri_df_path = (directory + 'dataframes/' + 'Book-3_Jacob-Obrecht_Monad_p-252_p-327.xml.pkl')

# Parse score with music21.
mto_score = music21.converter.parse(symbolic_score)

# NoteRest index the score (place the score into a pandas DataFrame
# that was parsed with music21.
vis_score = noterest.NoteRestIndexer(mto_score).run()

# saving dataframe
vis_score.to_pickle(nri_df_path)
df_from_pickle = pandas.read_pickle(nri_df_path)


# Find all the Horizontal intervals. 
hint_score = interval.HorizontalIntervalIndexer(df_from_pickle).run()

# Find all Vertical Intervals.
vint_score = interval.IntervalIndexer(vis_score).run()

# Find offset Vertical Intervals.
vint_o_dict = {'quarterLength':2.0, 'method': None}
vint_o_filt = offset.FilterByOffsetIndexer(vis_score,vint_o_dict).run()
vint_o_score = interval.IntervalIndexer(vint_o_filt).run()

# Find Ngrams.
hint_vint = pandas.concat([hint_score,vint_score],axis=1)
ngram_dict = {'mark singles': False, 'continuer': '1', 'n': 2}
ngram_dict['horizontal'] = [('interval.HorizontalIntervalIndexer','1')]
ngram_dict['vertical'] = [('interval.IntervalIndexer','0,1')]
ngrams_score = ngram.NGramIndexer(hint_vint,ngram_dict).run() 




