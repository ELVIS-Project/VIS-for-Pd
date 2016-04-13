# -*- coding: utf-8 -*-
"""
# ----- VIS-Tools.py ------------------------------------------------- #

A test function to test how the results of one python function can be 
passed to another in Pd.

Author:		Reiner Kramer	
Email:		reiner@music.org
Updated:	04.13.2016

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

	"""
	Parses a score through music21, and vis into a pandas DataFrame.
	"""

	# How many inlets and outlets.
	_inlets = 5
	_outlets = 1

	# Init function.
	def __init__(self,mto_score=0,ind_score=0,events=5,
		direction='beginning',slice_start=0,slice_end=3):
		"""
		Init function for storing variables used in this class.
		"""
		self.mto_score = mto_score
		self.ind_score = ind_score
		self.events = events
		self.direction = direction
		self.slice_start = slice_start
		self.slice_end = slice_end

	# Handling inlets.
	def _anything_1(self,symbolic_score):
		"""
		Parses a score in music21, then indexes the parsed score with 
		the vis-framework into a pandas DataFrame.
		"""
		try:
			the_score = music21.converter.parse(str(symbolic_score))
			self.mto_score = the_score
			print("The score has been parsed with music21.")
		except:
			print("Please load a symbolic score first.")

	def _anything_2(self,bang):
		"""
		If a "bang" was received in the second outlet the score is 
		NoteRest indexed.
		"""
		if(self.mto_score == 0):
			self._msg_missing_score()
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
		"""
		Determines how many events are to be shown.
		"""
		if(self.mto_score == 0):
			self._msg_missing_score()
		else:
			self.events = events
			# The beginning or the end of the DataFrame
			self._heads_or_tails()

	def _anything_4(self,direction):
		"""
		Determines, whether the events are shown from the beginning or 
		the end.
		"""
		if(self.mto_score == 0):
			self._msg_missing_score()
		else:
			self.direction = str(direction)
			self._heads_or_tails()

	def _anything_5(self,slice_start,slice_end):
		"""
		Picks a slice from a given DataFrame.
		"""
		if(self.mto_score == 0):
			self._msg_missing_score()
		else:
			print(self.ind_score.iloc[slice_start:slice_end])

	# Local methods: complying with DRY.
	def _heads_or_tails(self):
		"""
		Helper method to determine whether to count from the beginning
		or from the end of the DataFrame.
		"""
		if(self.direction == 'end'):
			print(self.ind_score.tail(self.events))
			#self._outlet(1,self.ind_score.tail(self.events).to_csv())
		else:
			print(self.ind_score.head(self.events))
			#self._outlet(1,self.ind_score.head(self.events).to_csv())

	def _msg_missing_score(self):
		"""
		Prints a message to the Pd window that a score has not been loaded.
		"""
		print("Please load a symbolic score first.")

# ----- END VIS-Tools.py --------------------------------------------- #
