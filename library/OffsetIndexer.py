# -*- coding: utf-8 -*-

"""
OffsetIndexer.py
================

Indexes passed-in DataFrames, assigns an offset, and creates a new off-
set DataFrame.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 11.19.2016

@TODO: 	The offsets currently happen at number of occuring offsets 
		rather than musical offsets. This needs to be changed to 
		musical offsets.

"""

import sys, os, music21, pandas, requests, vis, pyext
from vis.models.indexed_piece import Importer

try:
	print("OffIndexer.py was loaded.")
except:
	print("Loading OffIndexer.py failed.")


class Set(pyext._class):
	
	_inlets = 2
	_outlets = 2

	def __init__(self,
		symbolic_scores=0,
		scores_paths=0,
		scores_imported=[],
		events=5,
		df_offset=0):
		self.symbolic_scores = symbolic_scores
		self.scores_paths = scores_paths
		self.scores_imported = scores_imported
		self.events = events
		self.df_offset = df_offset


	def _anything_1(self, *symbolic_scores):
		"""
		Parses a pickeled DataFrame, and applies an offset to that Data-
		Frame as a new DataFrame.
		"""
		if(len(symbolic_scores) >= 1):

			try:

				self.scores_paths = [str(x) for x in symbolic_scores]

				for i in range(len(self.scores_paths)):
					self.scores_imported.append(
						pandas.read_pickle(self.scores_paths[i]))

				for x, y in zip(self.scores_paths,self.scores_imported):
					#self._generate_name(x)

					self._generate_name(x)

					y.columns.set_levels(['Part'], level=0, inplace=True)
					y.columns.set_names(['Score','Events'], inplace=True)
					print(y.head(self.events).to_csv(
							sep='\t',
							na_rep='^'))
			
			except Exception as e:
				
				print(e)
				#self._print_output('not_indexed')
		
		else:
		
			#self._print_output('no_scores')
			print("...there were no scores...")

	def _anything_2(self, offset):
		"""
		Takes a number to specify what type of offset to use. 
		Note: Check pandas documentation.
		"""
		self.df_offset = offset

		for x, y in zip(self.scores_paths,self.scores_imported):
			
			self._generate_name(x)
			y.columns.set_levels(['Part'], level=0, inplace=True)
			y.columns.set_names(['Score','Events'], inplace=True)
			
			if(self.df_offset == 0):
				print(y.head(self.events).to_csv(
					sep='\t',
					na_rep='^'))
			else:
				print(y[::self.df_offset].head(self.events).to_csv(
					sep='\t',
					na_rep='^'))

	def _generate_name(self,path):
		"""
		Private method to generate a human readable name of a composition 
		from its path.
		"""
		file_name = os.path.split(path)
		file_extr = os.path.splitext(file_name[1])
		comp_name = str(file_extr[0]).replace("-"," ").replace("_",": ")

		print("\n" + comp_name)
		print(len(comp_name) * "-")

