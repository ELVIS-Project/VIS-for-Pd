# -*- coding: utf-8 -*-
"""
CountMelodicIntervals.py
========================

A music21 filter to count melodic intervals of a composition.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 10.12.2016

"""

import sys, os, music21, pyext
from collections import Counter

try:
	print("CountMelodicIntervals.py was loaded.")
except:
	print("Loading CountMelodicIntervals.py failed.")

class Count(pyext._class):
	"""
	CountMelodicIntervals Module
	============================

	Count Class
	-----------

	Counts melodic intervals from a pickled music21 object.

	Inlets:

	1. Takes paths to pickled music21 files.
	2. Arguments to specify the sorting order of the interval counts.

	Outlets:
	
	1. The first outlet outputs the count.
	
	"""
	_inlets = 2
	_outlets = 1

	# Init function.
	def __init__(self,
		mto_scores=0,
		meta=0,
		melodic_intervals=0):
		"""
		Storing variables used in this class.
		"""
		self.mto_scores = mto_scores
		self.meta = meta
		self.melodic_intervals = melodic_intervals
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

				mel_int = music21.analysis.discrete.MelodicIntervalDiversity()
				mel_int_details = [mel_int.countMelodicIntervals(x,
					ignoreDirection=False) 
					for x in self.mto_scores]

				interval_tuples = [[(x, y[x][1]) 
					for x in list(y.keys())]
					for y in mel_int_details]

				self.melodic_intervals = [sorted(y, key=lambda x: x[1], reverse=True)
					for y in interval_tuples]

				self._print_interval_counts(self.melodic_intervals,self.meta)

			except ValueError:

				print(ValueError)

	def _anything_2(self, sort_by):
		"""
		Specifies the sort order of pitches.
		"""
		if(self.melodic_intervals == 0):

			print(self._msg_missing_scores())
		
		else:
			
			if(str(sort_by) == 'interval'):
				sorts_by = 0
				reversal = False
			else:
				sorts_by = 1
				reversal = True

			intervals_sorted = [sorted(y, key=lambda x: x[sorts_by], reverse=reversal)
				for y in self.melodic_intervals]
			
			self._print_interval_counts(intervals_sorted,self.meta)
			
	def bang_1(self):
		"""
		Checks wether or not a DataFrame exists or should be loaded.
		"""
		if(self.melodic_intervals == 0):

			print(self._msg_missing_scores())
		
		else:

			print("\nThe melodic interval counts were re-loaded.\n")
			self._print_interval_counts(self.melodic_intervals,self.meta)

	def _print_interval_counts(self, int_counts, meta):
		"""
		Prints the actual pitch counts to the Pd window.
		"""
		#pc_tupes = [x.items() for x in pc_counts]
		
		for x, z in zip(int_counts, meta):
			print "\n" + z + "\n" + len(z) * "-"
			for y in x:
				print(str(y[0]) + ":\t" + str(y[1]))


	def _msg_missing_scores(self):
		"""
		Method to indicate that no DataFrames have been loaded.
		"""
		return "Please load music21 streams first."

# ----- END CountPitches.py --------------------------------------- #