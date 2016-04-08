# -*- coding: utf-8 -*-
"""
# ----- NoteRestIndexing.py ------------------------------------------ #

A Python object to make the results of the NoteRestIndexer from the VIS
framework available to Pd.

Author:		Reiner Kramer	
Email:		reiner@music.org
Updated:	04.08.2016

Inlets:

1) The first inlet takes a symbolic score for input, which then will be 
first parsed with musicXML, and then placed into a dataframe.

Outlets:
1) The first outlet outputs a bang, when a csv version of the dataframe 
has been created along with a unique ID for that dataframe.
2) The second outlet displays status messages to the user.
3) The third outlet is provided for debugging purposes, but will be 
removed. 

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

class Index(pyext._class):
	"""
	Parses a score through music21, and vis into a pandas DataFrame.
	"""
	_inlets = 1
	_outlets = 3

	# Init function.
	def __init__(self,mto_score=0,ind_score=0):
		"""
		Init function for storing variables used in this class.
		"""
		self.mto_score = mto_score
		self.ind_score = ind_score
		# Messages
		self.err_msg_1 = "Please load a symbolic score first."
		self.err_msg_2 = "The NoteRestIndexer failed."
		self.mto_parsed = "The score was parsed with music21."
		self.vis_parsed = "The score has been indexed with VIS."
		self.vis_df_save = ("The DataFrame has been saved in the selected " +
			"format.")

	def _anything_1(self,symbolic_score):
		"""
		Parses a score in music21, then indexes the parsed score with 
		the vis-framework into a pandas DataFrame.
		"""
		try:
			# First parse the score with music21.
			the_score = music21.converter.parse(str(symbolic_score))
			self.mto_score = the_score
			# Change status, if successful and then try to place parsed
			# score into a dataframe.
			self._outlet(2, self.mto_parsed)

			try:
				indexed_score = noterest.NoteRestIndexer(self.mto_score).run()
				self.ind_score = indexed_score
				# Possible file formats:
				# to_csv() // as expected
				# to_json() // as expected
				# to_msgpack() // just like json ...
				# to_clipboard() > output bang?
				'''
				self._outlet(1, self.ind_score.to_csv(
					os.path.dirname(os.path.realpath(__file__)) + 
					'/dataframe.csv',
					na_rep="--",
					encoding='utf8'))
				'''
				self.ind_score.to_json(os.path.dirname(os.path.realpath(__file__)) + 
					'/dataframe.json')
				self._outlet(1, self.mto_parsed)
				self._outlet(2, self.vis_df_save)

			except:
				self._outlet(2, self.err_msg_2)

		except:
			self._outlet(2, self.err_msg_1)

# ----- END NoteRestIndexing.py -------------------------------------- #
