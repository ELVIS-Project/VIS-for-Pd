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

import sys, os, music21 

try:
	print("{} & {} loaded.".format(sys.argv, pyext))
except:
	print("Failed")

class mto(pyext._class):

	'''
	A musc21 class.
	'''

	_inlets = 1
	_outlets = 1

	def symbol_1(self,symbolic_score):
		parsed_score = music21.converter.parse(str(symbolic_score))
		self._outlet(1,parsed_score)

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

