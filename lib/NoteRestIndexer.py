# -*- coding: utf-8 -*-
"""
NoteRestIndexer.py
==================

A Python object to make the results of the NoteRestIndexer from the VIS
framework available to Pd.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 04.14.2016

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

class Index(pyext._class):
	"""
	NoteRestIndexer Module
	======================

	Index Class
	-----------

	Indexes a pickled music21 object in a pandas DataFrame.

	Inlets:

	1. The first inlet takes a list of pickled music21 objects, unthaws these
	objects, and then place them into a pandas DataFrame via the vis-framework.

	Outlets:
	
	1. The first outlet outputs a bang, and the packed dataframe.
	2. The second outlet displays status messages to the user. 
	
	"""
	_inlets = 1
	_outlets = 2

	# Init function.
	def __init__(self,mto_scores=0,ind_scores=0):
		"""
		Storing variables used in this class.
		"""
		self.mto_scores = mto_scores
		self.ind_scores = ind_scores
		# Messages
		self.err_msg_1 = ("There wasn't enough heat to thaw the frozen " + 
			"music21 object.")
		self.err_msg_2 = "The NoteRestIndexer failed."
		self.mto_parsed = "The scores were thawed and parsed with music21."
		self.vis_parsed = "The score has been indexed with VIS."

	def _anything_1(self,*pickled_scores):
		"""
		Parses a list of pickeled music21 scores, and indexes the scores with 
		the vis-framework into a pandas DataFrames.
		"""
		try:

			pickled = [str(x) for x in pickled_scores]
			unthawed = [music21.converter.thaw(pickled[i]) 
				for i in range(len(pickled))]
			local_msg = (self.mto_parsed + ": \n" + str([str(x) for x in unthawed]))
			self._outlet(2, local_msg)

		except:

			self._outlet(2, self.err_msg_1)

# ----- END NoteRestIndexer.py --------------------------------------- #
