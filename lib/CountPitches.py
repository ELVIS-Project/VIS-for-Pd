# -*- coding: utf-8 -*-
"""
CountPitches.py
==================

A music21 filter to count pitches of a composition.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 04.26.2016

"""

import sys, os, music21, pyext
from collections import Counter

try:
	print("CountPitches.py was loaded.")
except:
	print("Loading CountPitches.py failed.")

class Count(pyext._class):
	"""
	CountPitches Module
	======================

	Count Class
	-----------

	Counts pitches from a pickled music21 object.

	Inlets:

	1. Takes paths to pickled music21 files.

	Outlets:
	
	1. The first outlet outputs the count.
	
	"""
	_inlets = 1
	_outlets = 1

	# Init function.
	def __init__(self,
		mto_scores=0,
		ind_scores=0,
		df_paths=0,
		events=5,
		direction='beginning',
		slice_start=0,
		slice_end=5,
		meta=0):
		"""
		Storing variables used in this class.
		"""
		self.mto_scores = mto_scores
		self.meta = meta
		# Messages
		self.mto_parsed = "\nThe scores were thawed and parsed with music21."

	def _anything_1(self,*pickled_scores):
		"""
		Parses a list of pickeled music21 scores, and indexes the scores with 
		the vis-framework's NoteRestIndexer into pandas DataFrames.
		"""

		# print(pickled_scores)

		if(pickled_scores == 0):
			print(self._msg_missing_scores())

		else:

			try:

				pickled = [str(x) for x in pickled_scores]
				self.mto_scores = [music21.converter.thaw(pickled[i]) 
					for i in range(len(pickled))]

				self.meta = [(x.metadata.composer + " " + x.metadata.title) 
					for x in self.mto_scores]

				pc_counts = [x.pitchAttributeCount('midi') 
					for x in self.mto_scores]

				pc_tupes = [x.items() for x in pc_counts]

				pc_tupes_desc = [sorted(x, key=lambda y: y[0], reverse=True)
					for x in pc_tupes]

				for x, z in zip(pc_tupes_desc, self.meta):
					print "\n" + z + "\n" + len(z) * "-"
					for y in x:
						print(str(y[0]) + ":\t" + str(y[1]))
			
			except ValueError:
				print(ValueError)
			
	def bang_1(self):
		"""
		Checks wether or not a DataFrame exists or should be loaded.
		"""
		if(self.df_paths == 0):
			self._outlet(1, self._msg_missing_scores())
			print(self._msg_missing_scores())
		
		else:
			# self._outlet(1, "DataFrames exist.")
			print("The note-rest-indexed DataFrames were passed on.")
			self._outlet(1, [str(x) for x in self.df_paths])

	def _msg_missing_scores(self):
		"""
		Method to indicate that no DataFrames have been loaded.
		"""
		return "Please load music21 streams first."

	def _generate_name(self,path):
		"""
		Private method to generate a human readable name of a composition from
		it path.
		"""
		file_name = os.path.split(path)
		file_extr = os.path.splitext(file_name[1])
		comp_name = str(file_extr[0]).replace("-"," ").replace("_",": ")

		print("\n" + comp_name)
		print(len(comp_name) * "-")

# ----- END CountPitches.py --------------------------------------- #
