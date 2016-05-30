# -*- coding: utf-8 -*-
'''
# ----- Analysis.py -------------------------------------------------- #

Author: Reiner Kramer
Email:  reiner@music.org
Date:   05.29.2015

This is the main analysis script file used to find additional 
information on Piazzolla's Fugal Style.

# -------------------------------------------------------------------- #
'''

# Import music21.
import music21

# Import pandas.
import pandas

# Import vis-framework items.

# ----- working with pep installed vis ----- #
from vis.analyzers.indexers import noterest, interval, offset, ngram

# ----- Parsing a score ---------------------------------------------- #

# Basis VIS-Workflow

# Path to score.
symbolic_score = ('/Users/reiner/Desktop/MusCan-2016/vis/scores/'+
	'Fuga-y-Misterio-Expo.xml')

# Parse score with music21.
mto_score = music21.converter.parse(symbolic_score)

score_parts = [x.id for x in mto_score.parts]

# NoteRest index the score (place the score into a pandas DataFrame
# that was parsed with music21.
vis_score = noterest.NoteRestIndexer(mto_score).run()
# vis_score.columns.set_levels(parts, level=0, inplace=True)
# vis_score.columns.set_names(['Score','Events'], inplace=True)

vis_score

'''
# ----- built-in pandas items ----- # 
# Extracting one (a single part/voice) series:
vis_score['noterest.NoteRestIndexer']['0']
# Describe:
vis_score['noterest.NoteRestIndexer']['0'].describe()
# Instant Histograms:
vis_score['noterest.NoteRestIndexer']['0'].value_counts()
# Most counted value:
vis_score['noterest.NoteRestIndexer']['0'].mode()
# Get all values in a series as an array:
vis_score['noterest.NoteRestIndexer']['0'].values
# Checking amount of events in a series:
vis_score['noterest.NoteRestIndexer']['0'].size

# Converting pitch name values with music21
def convert_pitch(pitch, pitch_type):
	"""
	Converts a particular pitch name to another pitch name.
	- "pitch" must be for example: C#4
	- "pitch_type" is the convert-to value (see pitch.Pitch in music21) like:
	  pitchClass, name, nameWithOctave, midi, frequency, ps, fullName, french,
	  german, italian, spanish, unicodeName, unicodeNameWithOctave, octave, 
	  diatonicNoteNum, accidental, alter, microtone, step
	"""
	try:
		return getattr(music21.pitch.Pitch(pitch), pitch_type)
	except:
		return pitch

vis_score.applymap(lambda x: convert_pitch(x, 'pitchClass')).head(10)


# ... or just in the series:
vis_score['noterest.NoteRestIndexer']['0'].apply(lambda x: 
	convert_pitch(x, 'pitchClass'))

# ... in which case all the above examples for the series can be 'applied'
vis_score['noterest.NoteRestIndexer']['0'].apply(lambda x: 
	convert_pitch(x, 'pitchClass')).value_counts()
'''

# vis_pc_score = vis_score.applymap(lambda x: convert_pitch(x, 'pitchClass'))
# vis_midi_score = vis_score.applymap(lambda x: convert_pitch(x, 'midi'))
# vis_name_score = vis_score.applymap(lambda x: convert_pitch(x, 'name'))

# Find all the Horizontal intervals. 
hint_score = interval.HorizontalIntervalIndexer(vis_score).run()

# Find all Vertical Intervals.
vint_score = interval.IntervalIndexer(vis_score).run()

# Find offset Vertical Intervals.
vint_o_dict = {'quarterLength':4.0, 'method': None}
vint_o_filt = offset.FilterByOffsetIndexer(vis_score,vint_o_dict).run()
vint_o_score = interval.IntervalIndexer(vint_o_filt).run()

# Find Ngrams.
hint_vint = pandas.concat([hint_score,vint_score],axis=1)
ngram_dict = {'mark singles': False, 'continuer': '1', 'n': 3}
ngram_dict['horizontal'] = [('interval.HorizontalIntervalIndexer','3')]
ngram_dict['vertical'] = [('interval.IntervalIndexer','0,3'),
                          ('interval.IntervalIndexer','1,3'),
                          ('interval.IntervalIndexer','2,3')]
ngrams_score = ngram.NGramIndexer(hint_vint,ngram_dict).run() 




