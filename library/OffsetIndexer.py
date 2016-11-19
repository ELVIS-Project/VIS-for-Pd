# -*- coding: utf-8 -*-

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
		
		
		if(len(symbolic_scores) >= 1):

			try:

				self.scores_paths = [str(x) for x in symbolic_scores]

				for i in range(len(self.scores_paths)):
					self.scores_imported.append(
						pandas.read_pickle(self.scores_paths[i]))

				# Convert score paths from symbols to strings:
				#self.scores_paths = [str(x) for x in symbolic_scores]
				
				# Create Music21 streams and index them with VIS:
				#self.scores_imported = [Importer(x) for x in self.scores_paths]

				#print(self.scores_imported)

				for x, y in zip(self.scores_paths,self.scores_imported):
					#self._generate_name(x)
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

		self.df_offset = offset

		for x, y in zip(self.scores_paths,self.scores_imported):
			#self._generate_name(x)
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

