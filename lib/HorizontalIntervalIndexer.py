# -*- coding: utf-8 -*-
"""
HorizontalIntervalIndexer.py
============================

A Python object to interpret a NoteRestIndexed DataFrame. A new DataFrame is
created to find horizontal intervals in any given horizontal, or "melodic"
line via the VIS-Framework.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 04.26.2016

"""

import sys, os, music21, pyext, pandas

from vis.analyzers.indexers import noterest, interval

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
	creates a new DataFrame that shows all the horizontal intervals in a 
	particular part or stream. The main input type (inlet 1) is a 
	note-rest-indexed pickled DataFrame.

	"""
	_inlets = 6
	_outlets = 3

	def __init__(self,
		df_paths=0,
		df_scores=0,
		hint_df=0,
		events=5,
		direction='beginning',
		slice_start=0,
		slice_end=5,
		meta=5):
		"""
		Storing variables used in this class.
		"""
		self.df_paths = df_paths
		self.df_scores = df_scores
		self.hint_df = hint_df
		self.events = events
		self.direction = direction
		self.slice_start = slice_start
		self.slice_end = slice_end

	def _anything_1(self,*noterest_df):
		"""
		Parses a note-rest-indexed DataFrame and show horizontal intervals.
		"""
		
		try:
			msg = ("Horizontal interval music analysis:")
			print("\n" + msg + "\n" + len(msg) * "=")
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
			
			# Printing information to Pd window.
			for x, v, w in zip(self.df_paths,self.hint_df,self.df_scores):
				self._generate_name(x)
				print(v.head(self.events).to_csv(
					sep='\t',
					na_rep='^'))

			# Building, saving DataFrames to pass on.
			file_paths = []
			for x,y in zip(self.df_paths,self.hint_df):
				# Build the path names, and save them into a list variable.
				file_name = os.path.split(x)
				file_path = (os.path.dirname(os.path.realpath(__file__)) + 
					'/data/frames/hint/Hint_' + file_name[1])
				file_paths.append(file_path)
				# Save the dataframes as pickle(d) files.
				y.to_pickle(file_path)

			self._outlet(1, [str(x) for x in file_paths])

		except (RuntimeError, TypeError, NameError):
			print("O-M-G. Total Failure. Here's why:")
			print(RuntimeError, TypeError, NameError)

		except IOError:
			print("Please feed me a pickled NoteRestIndexer generated DataFrame.")

	def _anything_2(self,events):
		"""
		Determines how many events are to be shown.
		"""
		if(self.hint_df == 0):
			self._msg_missing_score()
		else:
			self.events = events
			# The beginning or the end of the DataFrame
			self._heads_or_tails()

	def _anything_3(self,direction):
		"""
		Determines, whether the events are shown from the beginning or 
		the end.
		"""
		if(self.hint_df == 0):
			self._msg_missing_score()
		else:
			self.direction = str(direction)
			self._heads_or_tails()

	def _anything_4(self,slice_start,slice_end):
		"""
		Picks a slice from a given DataFrame.
		"""
		if(self.hint_df == 0):
			self._msg_missing_score()
		else:
			for x, y in zip(self.df_paths,self.hint_df):
				self._generate_name(x)
				print(y.iloc[slice_start:slice_end].to_csv(
					sep='\t',
					na_rep='^'))

	def bang_1(self):
		"""
		Force pass DataFrame paths to next items, e.g.: filters.
		"""
		if(self.hint_df == 0):
			self._outlet(1, self._msg_missing_scores())
		
		else:
			# self._outlet(1, "DataFrames exist.")
			print("The horizontally indexed DataFrames were passed on.")
			self._outlet(1, [str(x) for x in self.hint_df])

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

	def _pd_window_msg(self,path):
		"""
		Private method to generate human readable messages for the Pd window.
		"""

		# Local methods: complying with DRY.
	def _heads_or_tails(self):
		"""
		Helper method to determine whether to count from the beginning
		or from the end of the DataFrame.
		"""
		for x, y in zip(self.df_paths,self.hint_df):
			
			self._generate_name(x)

			if(self.direction == 'end'):
				display = y.tail(self.events).to_csv(sep='\t', na_rep='^')
			
			else:
				display = y.head(self.events).to_csv(sep='\t', na_rep='^')
			
			print(display)

	def _msg_missing_scores(self):
		"""
		Method to indicate that no DataFrames have been loaded.
		"""
		return "Please load (a) note-rest-indexed DataFrame(s) first."





