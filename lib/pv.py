# -*- coding: UTF-8 -*-

"""
# ----- passing-values.py -------------------------------------------- #

A test function to test how the results of one python function can be 
passed to another in Pd.

Author:		Reiner Kramer	
Email:		reiner@music.org
Updated:	12.08.2015

# -------------------------------------------------------------------- #
"""

import sys, os, music21, pyext
from vis.analyzers.indexers import noterest

try:
	print("{} loaded.".format(sys.argv))
except:
	print("Failed")

class NoteRestIndexed(pyext._class):

	'''
	Parses a score through music21, and vis into a pandas DataFrame.
	'''

	_inlets = 1
	_outlets = 1

	def symbol_1(self,symbolic_score):
		'''
		Parses a score in music21, then indexes the parsed score with 
		the vis-framework into a pandas DataFrame.
		'''
		the_score = music21.converter.parse(str(symbolic_score))
		indexed_score = noterest.NoteRestIndexer(the_score).run()
		print indexed_score.head(5)

class PdWindowDisplay(pyext._class):
	'''
	Display options for a DataFrame (i.e.: indexed score).
	'''

	_inlets = 1
	_outlets = 1

	def symbol_1(self,df):
		'''
		Displays contents of DataFrame to the Pd window.
		'''

		print df


"""
def pass_value(mango):
	'''
	Passes a value.
	'''
	return mango

def catch_value(peach):
	'''
	Catches a value.
	'''
	return peach

def parse_score(symbolic_score):
	'''
	Parses a symbolic score with music21.
	'''
	parsed_score = music21.converter.parse(str(symbolic_score))
	return parsed_score

def catch_score(passed_score):
	'''
	Catches a music21 score object.
	'''
	print passed_score.show()
"""

