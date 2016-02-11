# -*- coding: utf-8 -*-
"""
# ----- VIS-Tools.py ------------------------------------------------- #

A test function to test how the results of one python function can be 
passed to another in Pd.

Author:		Reiner Kramer	
Email:		reiner@music.org
Updated:	02.11.2016

Todo: Lots ... Converting or dumping DataFrame into CSV?

# -------------------------------------------------------------------- #
"""

import sys, os, music21, pyext
from vis.analyzers.indexers import noterest

try:
        print("{} loaded.".format(sys.argv))
        print("Using Python {}.{}.{}.".format(
                sys.version_info[0],
                sys.version_info[1],
                sys.version_info[2]))
except:
	print("Failed")


        
class NoteRestIndexing(pyext._class):

	'''
	Parses a score through music21, and vis into a pandas DataFrame.
	'''

	# How many inlets and outlets.
	_inlets = 4
	_outlets = 1

	# Init function.
	def __init__(self,mto_score=0,ind_score=0,events=5,
		direction='beginning'):
		'''
		Init function for storing variables used in this class.
		'''
		self.mto_score = mto_score
		self.ind_score = ind_score
		self.events = events
		self.direction = direction

	# Handling inlets.
	def _anything_1(self,symbolic_score):
		'''
		Parses a score in music21, then indexes the parsed score with 
		the vis-framework into a pandas DataFrame.
		'''
		try:
			the_score = music21.converter.parse(str(symbolic_score))
			self.mto_score = the_score
			print("The score has been parsed with music21.")
		except:
			print("Please load a symbolic score first.")

	def _anything_2(self,bang):
		'''
		If a "bang" was received in the second outlet the score is 
		NoteRest indexed.
		'''
		if(self.mto_score == 0):
			print("Please load a symbolic score first.")
		else:
			if(bang):
				try:
					indexed_score = noterest.NoteRestIndexer(self.mto_score).run()
					self.ind_score = indexed_score
					print("The score has been indexed with the " + 
						"vis-framework.")
				except:
					print("Something went wrong with the" +
						"NoteRestIndexer.")

	def _anything_3(self,events):
		'''
		Determines how many events are to be shown.
		'''
		if(self.mto_score == 0):
			print("Please load a symbolic score first.")
		else:
			self.events = events
			self._heads_or_tails()

	def _anything_4(self,direction):
		'''
		Determines, whether the events are shown from the beginning or 
		the end.
		'''
		if(self.mto_score == 0):
			print("Please load a symbolic score first.")
		else:
			self.direction = str(direction)
			self._heads_or_tails()

	# Local method, to comply with DRY.
	def _heads_or_tails(self):
		'''
		Helper method to determine whether to count from the beginning
		or from the end of the DataFrame.
		'''
		if(self.direction == 'end'):
			print(self.ind_score.tail(self.events))
			#self._outlet(1,self.ind_score.tail(self.events).to_csv())
		else:
			print(self.ind_score.head(self.events))
			#self._outlet(1,self.ind_score.head(self.events).to_csv())

# ----- END VIS-Tools.py --------------------------------------------- #
