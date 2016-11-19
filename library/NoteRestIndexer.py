# -*- coding: utf-8 -*-

"""
NoteRestIndexer.py
==================

A Python object, making the results of the NoteRestIndexer from the VIS
framework available within Pd.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 11.19.2016

@TODO: 	Rather than saving dataframes as pickled files in the data folder
		of the library directory, files should be cached via memoization
		https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
		
"""

import sys, os, music21, pandas, requests, vis, pyext
from vis.models.indexed_piece import Importer

try:
	print("NoteRestIndexer.py was loaded.")
	print("Music21 Version: " + music21.__version__)
	print("VIS version: " + vis.__version__)

except:
	print("Loading NoteRestIndexer.py failed.")


class Index(pyext._class):
	"""
	NoteRestIndexer Module
	======================

	Index Class
	-----------

	Indexes computational symbolic music score into a pandas DataFrame.

	Inlets:

	1. The first inlet takes a list of symbolic music scores, and places them 
	   into a pandas DataFrame via the vis-framework.   
	   The first inlet also can take a bang in order to check whether or not a 
	   DataFrame exists.
	2. A bang queries to see how many scores have been indexed.

	Outlets:
	
	1. The first outlet outputs a bang, and the paths to the packed dataframes.
	2. The second outlet displays status messages to the user. 
	
	"""
	_inlets = 5
	_outlets = 3

	# Init function.
	def __init__(self,
		scores_paths=0,
		scores_imported=0,
		scores_mto=0,
		scores_mto_frozen=0,
		scores_pandas=0,
		df_paths=[],
		events=5,
		direction='beginning',
		slice_start=0,
		slice_end=5,
		meta=0):
		"""
		Storing variables used in this class.
		"""
		self.scores_paths = scores_paths
		self.scores_imported = scores_imported
		self.scores_mto = scores_mto
		self.scores_mto_frozen = scores_mto_frozen
		self.scores_pandas = scores_pandas
		self.df_paths = df_paths
		self.events = events
		self.direction = direction
		self.slice_start = slice_start
		self.slice_end = slice_end
		self.meta = meta
		self.mto_frozen_dir = (os.path.dirname(os.path.realpath(__file__)) 
			+ '/data/music21streams/')
	
	def _anything_1(self, *symbolic_scores):
		"""
		Parses a symbolic music score into a pandas DataFrame via VIS.
		"""
		if(len(symbolic_scores) >= 1):
			
			try:
				
				# Convert score paths from symbols to strings:
				self.scores_paths = [str(x) for x in symbolic_scores]
				
				# Create Music21 streams and index them with VIS:
				self.scores_imported = [Importer(x) for x in self.scores_paths]
				
				# Collect Music21 streams:
				self.scores_mto = [x._score for x in self.scores_imported]

				# Capture meta data from Music21 streams:
				self.meta = [(x.metadata.composer + "_" + 
					x.metadata.title).replace(" ", "-") 
					for x in self.scores_mto]

				# Freeze Music21 streams for later consumption:
				self.scores_mto_frozen = [music21.converter.freeze(
					self.scores_mto[i], fmt='pickle', fp=(self.mto_frozen_dir + 
					self.meta[i] + '.pgz'))
					for i in range(len(self.scores_mto))]

				# Create NoteRest indexed DataFrames of the scores:
				self.scores_pandas = [x.get_data('noterest') 
					for x in self.scores_imported]

				# Save NoteRestIndexed DataFrames:
				for i in range(len(self.scores_pandas)):
					
					# Build the path names, and save into a list.
					self.df_paths.append(
						os.path.dirname(os.path.realpath(__file__)) + 
						'/data/frames/noterest/' + self.meta[i] + '.pkl')

					# Save the dataframes as pickle(d) files.
					self.scores_pandas[i].to_pickle(self.df_paths[i])

				# Bang second outlet showing how many scores were indexed:
				self.bang_2()

				# Send paths to the noterest DataFrames to the first outlet:
				self._outlet(1, [str(x) for x in self.df_paths])
				
				# Renaming the columns to a more user friendly format:
				for x, y in zip(self.df_paths,self.scores_pandas):
					self._generate_name(x)
					y.columns.set_levels(['Part'], level=0, inplace=True)
					y.columns.set_names(['Score','Events'], inplace=True)
					print(y.head(self.events).to_csv(
						sep='\t',
						na_rep='^'))
				
				# Build a message to user that the operation was successful:
				self._print_output('indexed')
			
			except Exception as e:
				
				print(e)
				self._print_output('not_indexed')
		
		else:
		
			self._print_output('no_scores')
			
	def _anything_2(self,events):
		"""
		Determines how many events are to be shown.
		"""
		if(self.scores_pandas == 0):
			self._print_output('no_scores')
		else:
			self.events = events
			# The beginning or the end of the DataFrame
			self._heads_or_tails()

	def _anything_3(self,direction):
		"""
		Determines, whether the events are shown from the beginning or 
		the end.
		"""
		if(self.scores_pandas == 0):
			self._print_output('no_scores')
		else:
			self.direction = str(direction)
			self._heads_or_tails()

	def _anything_4(self,slice_start,slice_end):
		"""
		Picks a slice from a given DataFrame.
		"""
		if(self.scores_pandas == 0):
			self._print_output('no_scores')
		else:
			for x, y in zip(self.df_paths,self.scores_pandas):
				self._generate_name(x)
				y.columns.set_levels(['Part'], level=0, inplace=True)
				y.columns.set_names(['Score','Events'], inplace=True)
				print(y.iloc[slice_start:slice_end].to_csv(
					sep='\t',
					na_rep='^'))

	def bang_1(self):
		"""
		Checks wether or not a DataFrame exists or should be loaded.
		"""
		if(self.df_paths == 0):
			self._print_output('no_scores')

		else:
			# self._heads_or_tails()
			self._print_output('pass_on')
			self._outlet(1, [str(x) for x in self.df_paths])

	def bang_2(self):
		"""
		Check to see how many DataFrames exist, i.e. how many different scores
		were indexed. The number output can be used to select and individual 
		score for querying.
		"""
		try:
			self._outlet(2, len(self.scores_pandas))
		except Exception as e:
			#self._print_output('no_scores')
			print(e)

	def bang_5(self):
		"""
		Passes frozen Music21 scores onto music21 functions.
		"""
		if(self.scores_mto_frozen == 0):
			self._print_output('no_frozen')
		else:
			self._outlet(3, self.scores_mto_frozen)
	
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
	
	# Local methods:
	def _heads_or_tails(self):
		"""
		Helper method to determine whether to count from the beginning
		or from the end of the DataFrame.
		"""
		for x, y in zip(self.df_paths,self.scores_pandas):
			
			self._generate_name(x)

			y.columns.set_levels(['Part'], level=0, inplace=True)
			y.columns.set_names(['Score','Events'], inplace=True)

			if(self.direction == 'end'):
				display = y.tail(self.events).to_csv(sep='\t', na_rep='^')
			
			else:
				display = y.head(self.events).to_csv(sep='\t', na_rep='^')
			
			print(display)

	def _print_output(self,print_what):
		"""
		Selects and formats message outputs in the Pd window.
		"""
		messages = {
			'indexed':'\nThe scores have been indexed with VIS.',
			'not_indexed':'\nThe score(s) have not indexed with VIS.',
			'no_scores':'\nA symbolic music score is required.',
			'pass_on':'\nThe note-rest-indexed DataFrames were passed on.',
			'nri_fail':'\nThe NoteRestIndexer failed.',
			'music21_fail':'\nMusic21 failed to unthaw the music21 streams.',
			'no_frozen':'\nThere are no Music21 streams available'
		}

		print(messages[print_what])

# ----- END NoteRestIndexer.py --------------------------------------- #
