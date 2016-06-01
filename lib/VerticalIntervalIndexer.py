# -*- coding: utf-8 -*-
"""
VerticalIntervalIndexer.py
==========================

A Python object to interpret a NoteRestIndexed DataFrame. A new DataFrame is
created to find vertical intervals in any given sounding simultaneity
line via the VIS-Framework.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 05.29.2016

"""

import sys, os, music21, pyext, pandas
from vis.analyzers.indexers import noterest, interval

try:
	print("VerticalIntervalIndexer.py was loaded.")
except:
	print("Loading VerticalIntervalIndexer.py failed.")

class Get(pyext._class):
	"""
	VerticalIntervalIndexer Module
	================================

	Get
	---

	Processes a DataFrame generated by the NoteRestIndexer, parses it, and 
	creates a new DataFrame that shows all the vertical intervals in a stream.
	The main input type (inlet 1) is a note-rest-indexed pickled DataFrame.

	"""
	_inlets = 6
	_outlets = 2

	def __init__(self,
		nri_df=0,
		df_paths=0,
		df_scores=0,
		vint_df=0,
		events=5,
		direction='beginning',
		slice_start=0,
		slice_end=5,
		meta=5,
		vint_settings=0,
		vint_paths=0):
		"""
		Storing variables used in this class.
		"""
		self.nri_df = nri_df
		self.df_paths = df_paths
		self.df_scores = df_scores
		self.vint_df = vint_df
		self.events = events
		self.direction = direction
		self.slice_start = slice_start
		self.slice_end = slice_end
		self.meta = meta
		self.vint_settings = {

			'simple or compound':'simple',
			'quality': False,
			'directed': True,
			'mp':False,
			'horiz_attach_later':False

		}
		self.vint_paths = vint_paths

	def _anything_1(self,*noterest_df):
		"""
		Parses a note-rest-indexed DataFrame and shows vertical intervals.
		"""
		
		try:
			msg = ("Vertical interval music analysis:")
			print("\n" + msg + "\n" + len(msg) * "=")
			
			# Counting through the dataframes and converting symbols to paths:
			self.df_paths = [str(x) for x in noterest_df]

			# Choosing DataFrame:
			self.df_scores = [pandas.read_pickle(self.df_paths[i]) 
				for i in range(len(self.df_paths))]
			
	   		# Showing the vertical intervals.
			# settings = {'mp':False,'horiz_attach_later':False}	
			self.vint_df = [interval.IntervalIndexer(x,
				self.vint_settings).run() for x in self.df_scores]
			
			for x, v, w in zip(self.df_paths,self.vint_df,self.df_scores):
				
				file_name = os.path.split(x)
				file_extr = os.path.splitext(file_name[1])
				comp_name = str(file_extr[0]).replace("-"," ")

				print("\n" + comp_name.replace("_",": "))
				print(len(comp_name) * "-")

				v.columns.set_levels(['Part'], level=0, inplace=True)
				v.columns.set_names(['Score','Events'], inplace=True)

				print(v.head(self.events).to_csv(
					sep='\t',
					na_rep='^'))

			# Building, saving DataFrames to pass on.
			self.vint_paths = []

			for x,y in zip(self.df_paths,self.vint_df):
				# Build the path names, and save them into a list variable.
				file_name = os.path.split(x)
				file_path = (os.path.dirname(os.path.realpath(__file__)) + 
					'/data/frames/vint/Vint_' + file_name[1])
				self.vint_paths.append(file_path)
				# Save the dataframes as pickle(d) files.
				y.to_pickle(file_path)

			# Passing on VINT DataFrames
			self._outlet(1, [str(x) for x in self.vint_paths])
			# Passing through Noterest Indexed DataFrames
			self._outlet(2, [str(x) for x in self.df_paths])
			
		except Exception as e:
			
			print(e)

	def _anything_2(self,events):
		"""
		Determines how many events are to be shown.
		"""
		if(self.vint_df == 0):
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
		if(self.vint_df == 0):
			self._msg_missing_score()
		else:
			self.direction = str(direction)
			self._heads_or_tails()

	def _anything_4(self,slice_start,slice_end):
		"""
		Picks a slice from a given DataFrame.
		"""
		if(self.vint_df == 0):
			self._msg_missing_score()
		else:
			for x, y in zip(self.df_paths,self.vint_df):
				self._generate_name(x)
				y.columns.set_levels(['Part'], level=0, inplace=True)
				y.columns.set_names(['Score','Events'], inplace=True)
				print(y.iloc[slice_start:slice_end].to_csv(
					sep='\t',
					na_rep='^'))

	def _anything_5(self,*vint_settings):
		"""
		Settings as adopted from the VIS-framework.
		"""
		self.vint_settings = {

			'simple or compound': str(vint_settings[0]),
			'quality': eval(str(vint_settings[1])),
			'directed': eval(str(vint_settings[2])),
			'mp': eval(str(vint_settings[3])),
			'horiz_attach_later': eval(str(vint_settings[4]))		

		}

		# Re-Generating vertical DataFrame Index 
		self.vint_df = [interval.IntervalIndexer(x,
			self.vint_settings).run() for x in self.df_scores]
		
		self._heads_or_tails()

	def _heads_or_tails(self):
		"""
		Helper method to determine whether to count from the beginning
		or from the end of the DataFrame.
		"""
		for x, y in zip(self.df_paths,self.vint_df):
			
			self._generate_name(x)

			y.columns.set_levels(['Part'], level=0, inplace=True)
			y.columns.set_names(['Score','Events'], inplace=True)

			if(self.direction == 'end'):
				display = y.tail(self.events).to_csv(sep='\t', na_rep='^')
			
			else:
				display = y.head(self.events).to_csv(sep='\t', na_rep='^')
			
			print(display)

	def _generate_name(self,path):
		"""
		Private method to generate a human readable name of a composition from
		it path.
		"""
		file_name = os.path.split(path)
		file_extr = os.path.splitext(file_name[1])
		comp_name = str(file_extr[0]).replace("-"," ").replace("_",": ")

		return comp_name

	def _pd_window_msg(self,path):
		"""
		Private method to generate human readable messages for the Pd window.
		"""
