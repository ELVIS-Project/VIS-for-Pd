# -*- coding: utf-8 -*-
"""
# ----- DataFrameExpand.py ------------------------------------------ #

A Python object to make the results of the NoteRestIndexer from the VIS
framework available to Pd.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 02.12.2016

Inlets:

1) The first inlet takes a pandas dataframe input.

Outlets:


# -------------------------------------------------------------------- #
"""

import sys, os, music21, pyext, pandas
from vis.analyzers.indexers import noterest

try:
    print("{} loaded.".format(sys.argv))
    print("Using Python {}.{}.{}.".format(
    	sys.version_info[0],
    	sys.version_info[1],
    	sys.version_info[2]))
except:
	print("Failed")

class Unpack(pyext._class):
	'''
	Unpacks a DataFrame.
	'''
	_inlets = 1
	_outlets = 2

	def __init__(self,df_score=0):
		'''
		Init function for the Unpack class.
		'''
		self.df_score = df_score
		self.status_msg_pass = "The dataframe unpack succeeded."
		self.status_msg_fail = "The dataframe unpack failed."

	def _anything_1(self,passed_in_df):
		
		try:
			the_data = (os.path.dirname(os.path.realpath(__file__)) + 
				'/dataframe.csv')
			the_score = pandas.read_csv(
				the_data,
				header=0,
				names=['soprano','alto','tenor','bass'], 
				index_col=0,
				encoding='utf-8')
			self._outlet(1, the_score.tail(10).to_csv(sep=" "))
			self._outlet(2, self.status_msg_pass)

		except:
			self._outlet(2, self.status_msg_fail)

		"""
		if(bang.split(':') ==)
		try:
			self._outlet(1, bang)
			self._outlet(2, self.status_msg_pass)
		except:
			self._outlet(2, self.status_msg_fail)
		"""
