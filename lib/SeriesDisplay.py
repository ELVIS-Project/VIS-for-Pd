# -*- coding: utf-8 -*-
"""
SeriesDisplay.py
================

Can take any DataFrame and display a selected series.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 05.26.2016

"""

import sys, os, music21, pyext, pandas

from vis.analyzers.indexers import noterest, interval

try:
	print("SeriesDisplay.py was loaded.")
except:
	print("SeriesDisplay.py failed.")

class Select(pyext._class):
	"""
	SeriesDisplay Module
	====================

	Select
	------
	Selects any individual series from a DataFrame.
	"""

	_inlets = 5
	_outlets = 1

	def __init__(self,
		nri_df = 0,
		df_paths = 0,
		df_scores = 0,
		df_series = 0):
		"""
		Local variables for the 'select' class.
		"""
		self.nri_df = nri_df
		self.df_paths = df_paths
		self.df_scores = df_scores
		self.df_series = df_series

	def _anything_1(self,*data_frames):
		"""
		Opens DataFrames (NoteRestIndexed DataFrames for now). 
		"""

		try:

			self.nri_df = data_frames
			# Converting symbols to strings:
			self.df_paths = [str(x) for x in self.nri_df]
			# Un-pickeling DataFrames:
			self.df_scores = [pandas.read_pickle(x) 
				for x in self.df_paths]
			# Determining series per DataFrame:
			self.df_series = [len(x.columns) for x in self.df_scores]
			
			# Debug print:
			print("The following DataFrames have been processed: {0}.".format(
				self.df_paths))
			print("The DataFrame consists of {0} series".format(
				self.df_series))

		except Exception as e:
			print(e)



# ----- SeriesDisplay.py ---------------------------------------------------- #