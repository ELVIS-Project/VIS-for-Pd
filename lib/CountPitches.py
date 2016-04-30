# -*- coding: utf-8 -*-
"""
CountPitches.py
==================

A music21 filter to count pitches of a composition.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 04.29.2016

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
	2. The inlet can be used how the pitches should be named.
	3. Arguments to specify the sorting order of the pitch counts.

	Outlets:
	
	1. The first outlet outputs the count.
	
	"""
	_inlets = 3
	_outlets = 1

	# Init function.
	def __init__(self,
		mto_scores=0,
		meta=0,
		pc_counts=0,
		pitch_id='nameWithOctave'):
		"""
		Storing variables used in this class.
		"""
		self.mto_scores = mto_scores
		self.meta = meta
		self.pc_counts = pc_counts
		self.pitch_id = pitch_id
		# Messages
		self.mto_parsed = "\nThe scores were thawed and parsed with music21."

	def _anything_1(self,*pickled_scores):
		"""
		Counts pitches in a pickled list of music21 scores.
		"""
		if(pickled_scores == 0):
			print(self._msg_missing_scores())

		else:

			try:

				pickled = [str(x) for x in pickled_scores]

				self.mto_scores = [music21.converter.thaw(pickled[i]) 
					for i in range(len(pickled))]

				self.meta = [(x.metadata.composer + ": " + x.metadata.title) 
					for x in self.mto_scores]

				self.pc_counts = [x.pitchAttributeCount(self.pitch_id) 
					for x in self.mto_scores]

				self._print_pitch_counts(self.pc_counts,self.meta)
			
			except ValueError:

				print(ValueError)

	def _anything_2(self, pitch_identification):
		"""
		Specify what type of pitch names to display. Options are music21 
		options: pitchClass, name, nameWithOctave, midi.
		"""
		self.pitch_id = str(pitch_identification)
		self.pc_counts = [x.pitchAttributeCount(self.pitch_id) 
			for x in self.mto_scores]

		self._print_pitch_counts(self.pc_counts,self.meta)

	def _anything_3(self, sort_by):
		"""
		Specifies the sort order of pitches.
		"""
		if(self.pc_counts == 0):

			print(self._msg_missing_scores())
		
		else:
		
			if(str(sort_by) == 'pitch'):
				sorts_by = 1
				reversal = False
			else:
				sorts_by = 2
				reversal = True

			self.pc_counts = [x.pitchAttributeCount(self.pitch_id) 
				for x in self.mto_scores]

			pc_tupes = [x.items() for x in self.pc_counts]

			pc_tupes_midi = [[(x[0], music21.pitch.Pitch(x[0]).midi, x[1]) 
				for x in y] 
				for y in pc_tupes]
			
			pc_sorted = [sorted(y, key=lambda x: x[sorts_by], reverse=reversal)
				for y in pc_tupes_midi]
			
			for x, z in zip(pc_sorted, self.meta):
				print "\n" + z + "\n" + len(z) * "-"
				for y in x:
					print(str(y[0]) + ":\t" + str(y[2]))
			

			# print pc_sorted
		# self.pc_counts = dict((x, y) for x, y in pc_tupes_desc)

		# self._print_pitch_counts(self.pc_counts,self.meta)
			
	def bang_1(self):
		"""
		Checks wether or not a DataFrame exists or should be loaded.
		"""
		if(self.pc_counts == 0):

			print(self._msg_missing_scores())
		
		else:

			print("\nThe pitch counts were re-loaded.\n")
			self._print_pitch_counts(self.pc_counts,self.meta)

	def _print_pitch_counts(self, pc_counts, meta):
		"""
		Prints the actual pitch counts to the Pd window.
		"""
		pc_tupes = [x.items() for x in pc_counts]
		
		for x, z in zip(pc_tupes, meta):
			print "\n" + z + "\n" + len(z) * "-"
			for y in x:
				print(str(y[0]) + ":\t" + str(y[1]))


	def _msg_missing_scores(self):
		"""
		Method to indicate that no DataFrames have been loaded.
		"""
		return "Please load music21 streams first."

# ----- END CountPitches.py --------------------------------------- #