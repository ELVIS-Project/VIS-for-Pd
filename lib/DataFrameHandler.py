# -*- coding: utf-8 -*-
"""
# ----- DataFrameHandler.py ------------------------------------------ #

A Python object to make the results of the NoteRestIndexer from the VIS
framework available to Pd.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 04.12.2016

Inlets:

1) The first inlet takes a symbolic score for input, which then will be 
first parsed with musicXML, and then placed into a dataframe.

Outlets:
1) The first outlet outputs a bang, and the packed dataframe.
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

class Pack(pyext._class):
	'''
	Packs a music21 score into DataFrame.
	'''
	_inlets = 1
	_outlets = 4

	# Init function.
	def __init__(self,mto_score=0,ind_score=0):
		'''
		Init function for storing variables used in this class.
		'''
		self.mto_score = mto_score
		self.ind_score = ind_score
		# Messages
		self.err_msg_1 = "Please load a symbolic score first."
		self.err_msg_2 = "The NoteRestIndexer failed."
		self.mto_parsed = "The score was parsed with music21."
		self.vis_parsed = "The score has been indexed with VIS."

	def _anything_1(self,symbolic_score):
		'''
		Parses a score in music21, then indexes the parsed score with 
		the vis-framework into a pandas DataFrame.
		'''
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
				# Write the dataframe to CSV.
				self.ind_score.to_csv(
					os.path.dirname(os.path.realpath(__file__)) + 
					'/Alma-dataframe.csv',
					#na_rep="--",
					encoding='utf-8')
				# Pickle the dataframe.
				"""
				self.ind_score.to_pickle(
					os.path.dirname(os.path.realpath(__file__)) + 
					'/Alma-dataframe.pkl')
				
				# Put dataframe into JSON.
				self.ind_score.to_json(
					os.path.dirname(os.path.realpath(__file__)) + 
					'/Alma-dataframe.json')
				"""

				# Pass the CSV dataframe path the right left outlet
				
				self._outlet(1, str(os.path.dirname(os.path.realpath(__file__)) + 
					'/Alma-dataframe.csv'))				
				self._outlet(2, self.vis_parsed)
				self._outlet(3, self.ind_score.head(5).to_csv(
					sep=" ",
					na_rep="--", 
					encoding='utf-8'))

			except:
				self._outlet(2, self.err_msg_2)

		except:
			self._outlet(2, self.err_msg_1)

# ----- END DataFrameHandler.py -------------------------------------- #
