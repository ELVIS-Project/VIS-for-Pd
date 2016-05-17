# -*- coding: utf-8 -*-
'''
# ----- Analysis.py -------------------------------------------------- #

Author: Reiner Kramer
Email:  reiner@music.org
Date:   05.17.2016

This is the main analysis script file used to create the Mode-Finder
program. The purpose is to create a set of algorithms that can be used 
to build a heuristic mode finding algorithm based on Glarean's 
Dodecachordon. The algorithm in turn can be used to analyze and group
period compositions (i.e. by composers mentioned by Glarean, and other
contemporary composers).

# -------------------------------------------------------------------- #
'''

# Import music21, and pandas
import music21, pandas, sys

# Import vis-framework items.
from vis.analyzers.indexers import noterest, interval, offset, ngram

from collections import Counter

# ----- Parsing a score ---------------------------------------------- #

# Basic VIS-Workflow

# Path to score.

directory = ('/Users/reiner/Documents/MusicAnalyses/VIS-for-Pd/scores/'
	+ 'monophonic/symbolic/')


symbolic_score = (directory + 'Book-1_Ave-Maria-benedicta-tu_p-146.xml')
# symbolic_score = (directory + 'Book-1_Dominus-vobiscum_pp-146-47.xml')

nri_df_path = (directory + 'dataframes/' + 
	'Book-1_Ave-Maria-benedicta-tu_p-146.pkl')

# Parse score with music21.
mto_score = music21.converter.parse(symbolic_score)

# Looking at the first 5 pitches of a score
first_five = [str(x) for x in mto_score.parts[0].pitches[:5]]

# ----- Counting Pitches ------ #
#pc_count = mto_score.pitchAttributeCount('pitchClass')
# pc_name_count = mto_score.pitchAttributeCount('name')
pc_count = mto_score.pitchAttributeCount('nameWithOctave')

# putting pc_count dictionary into tuplet format
pc_count_tup = [(x, pc_count[x]) for x in list(pc_count.keys())]
# pc_name_count_tup = [(x, pc_name_count[x]) for x in list(pc_name_count.keys())]
# ps_name_count_tup = [(x, ps_name_count[x]) for x in list(ps_name_count.keys())]

# sorting according to pitch names ascending
pc_count_sorted = sorted(pc_count_tup, key=lambda x: x[0])

# sorting according to pitch names descening
pc_count_sorted_desc = sorted(pc_count_tup, key=lambda x: x[0], reverse=True)

# sorting according to pitch occurence ascending
pc_count_sort_occ = sorted(pc_count_tup, key=lambda x: x[1])

# sorting according to pitch occurence descending
pc_count_sort_occ_desc = sorted(pc_count_tup, key=lambda x: x[1], reverse=True)

# ----- End counting pitches ----- #

# ----- Getting the Key Signature of a piece ----- #

parts_num = len(mto_score.parts)
key_signature = mto_score.parts[parts_num-1].measure(1).keySignature
# <music21.key.KeySignature of 1 flat>
# key_signature.sharps
# -1

# ----- END Key Signature ----- #

# ----- Transpose and entire Piece ----- #
# up by a perfect fifth ... for all parts
t_mto_score = mto_score.transpose('p5')
# individual parts would be mto_score.parts[0].transpose('-p4')

# ----- END Key Transposition ----- #

# ----- Ambitus ----- #
ambana = music21.analysis.discrete.Ambitus()
ambana.getPitchRanges(t_mto_score)
# (0, 12)
ambana.getPitchSpan(t_mto_score)
# (<music21.pitch.Pitch D3>, <music21.pitch.Pitch D4>)
# in MIDI: [x.midi for x in ambana.getPitchSpan(mto_score)]
# in PS Names: [x.nameWithOctave for x in ambana.getPitchSpan(mto_score)]
ambana.getSolution(mto_score)
# <music21.interval.Interval P8>
# ambana.getSolution(mto_score).name
# 'P8'

# ----- END Ambitus ----- #

# ----- Counting Melodic Intervals ----- #
mel_int_div = music21.analysis.discrete.MelodicIntervalDiversity()
mel_int_count = mel_int_div.countMelodicIntervals(mto_score)
mel_int_detail = mel_int_div.countMelodicIntervals(mto_score,
	ignoreDirection=False)
# returns a dictionary
"""
{'m2': [<music21.interval.Interval m2>, 37], 
	'M2': [<music21.interval.Interval M2>, 95], 
	'M3': [<music21.interval.Interval M3>, 3], 
	'm3': [<music21.interval.Interval m3>, 11], 
	'P5': [<music21.interval.Interval P5>, 8]}
"""
mel_int_tup =  [(x, mel_int_count[x][1]) 
	for x in list(mel_int_count.keys())]

mel_int_detail_tup = [(x, mel_int_detail[x][1]) 
	for x in list(mel_int_detail.keys())]

# sorting
mel_int_sort_val = sorted(mel_int_tup, 
	key=lambda x: x[1], reverse=False)

mel_int_sort_val_desc = sorted(mel_int_tup, 
	key=lambda x: x[1], reverse=True)

# with detailed views
meli_det_sort_val = sorted(mel_int_detail_tup, 
	key=lambda x: x[1], reverse=False)

meli_det_sort_val_desc = sorted(mel_int_detail_tup, 
	key=lambda x: x[1], reverse=True)

"""
print("\n")
for x in meli_det_sort_val:
 	print(x[0] + ": \t" + str(x[1]))
"""
# ----- END Melodic Intervals ----- #

# NoteRest index the score (place the score into a pandas DataFrame
# that was parsed with music21.
vis_score = noterest.NoteRestIndexer(mto_score).run()
t_vis_score = noterest.NoteRestIndexer(t_mto_score).run()

# saving dataframe
vis_score.to_pickle(nri_df_path)
df_from_pickle = pandas.read_pickle(nri_df_path)

# Find all the Horizontal intervals. 

# Settings
hint_settings = {
	'simple or compound':'simple',
	'quality': True,
	'directed': True,
	'horiz_attach_later': True,
	'mp':False
}

hint_score = interval.HorizontalIntervalIndexer(df_from_pickle,hint_settings).run()


# Find N-Grams from Horizontal Intervals 

def horizontal_ngrams(hint_score,sample_rate):
	"""
	Create only horizontal N-Grams, specifically for monophonic pieces.
	"""
	hint_col = [str(x) 
		for x in hint_score['interval.HorizontalIntervalIndexer']['0']
		if (str(x) != 'Rest')]

	hint_col_ng = []

	for x in range(len(hint_col)):
		if x < (len(hint_col) - (sample_rate - 1)):
			hint_col_ng.append(hint_col[x:(x+sample_rate)])

	return hint_col, hint_col_ng

hints_ngrams = horizontal_ngrams(hint_score, 5)

def count_unique_ngrams(hints_ngrams,ordered=True):
	"""
	Counts N-Grams, removes duplicates, and sorts them in order of frequency.
	"""
	counted_ngrams = [(x, hints_ngrams.count(x)) for x in hints_ngrams]
	reduced_ngrams = [eval(y) for y in set([str(x) for x in counted_ngrams])]

	if(ordered == True):
		
		ordered_ngrams = sorted(reduced_ngrams, 
			key=lambda x: x[1], 
			reverse=True)
		
		return ordered_ngrams
	
	else:
		
		return reduced_ngrams

unique_ngrams = count_unique_ngrams(hints_ngrams[1],ordered=True)

"""
print('\n')
for x in unique_ngrams:
	print(str(x[1]) + '\t' + str(x[0]))
"""
# -------------------------------------------------------------------- #

"""
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
"""