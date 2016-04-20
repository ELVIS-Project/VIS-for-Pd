# -*- coding: utf-8 -*-
"""
HorizontalIntervalIndexer.py
============================

A Python object to to interpret a NoteRestIndexed DataFrame. A new DataFrame is
created to find horizontal intervals in any given horizontal, or "melodic"
line via the VIS-Framework.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 04.20.2016

"""

import sys, os, music21, pyext, pandas

from vis.analyzers.indexers import noterest
from vis.analyzers.indexers import interval

try:
	print("HorizontalIntervalIndexer.py was loaded.")
except:
	print("Loading HorizontalIntervalIndexer.py failed.")

class Get(pyext._class):
	"""
	HorizontalIntervalIndexer Module
	================================

	Get
	---

	Processes a DataFrame generated by the NoteRestIndexer, parses it, and 
	creates a new DataFrame that show all the horizontal intervals in a 
	particular part or stream.

	"""
	_inlets = 3
	_outlets = 3

	def __init__(self,df_paths=0,df_scores=0,hint_df=0):
		"""
		Storing variables used in this class.
		"""
		self.df_paths = df_paths
		self.df_scores = df_scores
		self.hint_df = hint_df

	def _anything_1(self,*noterest_df):
		"""
		Parses a note-rest-indexed DataFrame and show horizontal intervals.
		"""
		
		try:
			msg = ("Starting new music analysis.")
			print("\n" + len(msg) * "=")
			print(msg)
			print(len(msg) * "=")
			# Counting through the dataframes and converting symbols to paths:
			self.df_paths = [str(x) for x in noterest_df]

			# Choosing DataFrame:
			self.df_scores = [pandas.read_pickle(self.df_paths[i]) 
				for i in range(len(self.df_paths))]
			
	   		# Showing the horizontal intervals.
			# not sure why mulitprocessing has to be turned off :-/
			settings = {'mp':False,'horiz_attach_later':False}	
			self.hint_df = [interval.HorizontalIntervalIndexer(x,
				settings).run() for x in self.df_scores]
			
			for v, w in zip(self.hint_df,self.df_scores):
				print(w.head(5).to_csv(sep=' '))
				print(v.head(5).to_csv(sep=' '))

		except (RuntimeError, TypeError, NameError):
			print("O-M-G. Total Failure. Here's why:")
			print(RuntimeError, TypeError, NameError)
