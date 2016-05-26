# -*- coding: utf-8 -*-
"""
NoteRestIndexer.py
==================

A Python object to make the results of the NoteRestIndexer from the VIS
framework available to Pd.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 05.25.2016

"""

import sys, os, music21, pyext
from vis.analyzers.indexers import noterest

try:
	print("NoteRestIndexer.py was loaded.")
except:
	print("Loading NoteRestIndexer.py failed.")

class Index(pyext._class):
	"""
	NoteRestIndexer Module
	======================

	Index Class
	-----------

	Indexes a pickled music21 object in a pandas DataFrame.

	Inlets:

	1. The first inlet takes a list of pickled music21 objects, unthaws these
	objects, and then place them into a pandas DataFrame via the vis-framework.
	The first inlet also can take a bang in order to check whether or not a 
	DataFrame exists.
	2. A bang queries to see how many scores have been indexed.

	Outlets:
	
	1. The first outlet outputs a bang, and the paths packed dataframe.
	2. The second outlet displays status messages to the user. 
	
	"""
	_inlets = 6
	_outlets = 2

	# Init function.
	def __init__(self,
		mto_scores=0,
		ind_scores=0,
		df_paths=0,
		events=5,
		direction='beginning',
		slice_start=0,
		slice_end=5,
		meta=0):
		"""
		Storing variables used in this class.
		"""
		self.mto_scores = mto_scores
		self.ind_scores = ind_scores
		self.df_paths = df_paths
		self.events = events
		self.direction = direction
		self.slice_start = slice_start
		self.slice_end = slice_end
		self.meta = meta

	def _anything_1(self,*pickled_scores):
		"""
		Parses a list of pickeled music21 scores, and indexes the scores with 
		the vis-framework's NoteRestIndexer into pandas DataFrames.
		"""

		if(pickled_scores == 0):
			self._print_output('no_scores')

		else:

			try:

				pickled = [str(x) for x in pickled_scores]
				unthawed = [music21.converter.thaw(pickled[i]) 
					for i in range(len(pickled))]

				self.meta = [(x.metadata.composer + "_" + 
					x.metadata.title).replace(" ", "-") 
					for x in unthawed]

				try:

					self.ind_scores = [noterest.NoteRestIndexer(i).run()
						for i in unthawed]

					self.df_paths = []

					for i in range(len(self.ind_scores)):
						
						# Build the path names, and save into a list.
						self.df_paths.append(
							os.path.dirname(os.path.realpath(__file__)) + 
							'/data/frames/noterest/' + self.meta[i] + '.pkl')

						# Save the dataframes as pickle(d) files.
						self.ind_scores[i].to_pickle(self.df_paths[i])

					self.bang_2()
					self._outlet(1, [str(x) for x in self.df_paths])
					# self._print_output('mto_parsed')

					for x, y in zip(self.df_paths,self.ind_scores):
						self._generate_name(x)
						# Renaming the columns to a more user friendly format.
						y.columns.set_levels(['Part'], level=0, inplace=True)
						y.columns.set_names(['Score','Events'], inplace=True)
						print(y.head(self.events).to_csv(
							sep='\t',
							na_rep='^'))

					self._print_output('vis_parsed')

				except:

					self._print_output('nri_fail')

			except:

				self._print_output('music21_fail')
				

	def _anything_2(self,events):
		"""
		Determines how many events are to be shown.
		"""
		if(self.ind_scores == 0):
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
		if(self.ind_scores == 0):
			self._print_output('no_scores')
		else:
			self.direction = str(direction)
			self._heads_or_tails()

	def _anything_4(self,slice_start,slice_end):
		"""
		Picks a slice from a given DataFrame.
		"""
		if(self.ind_scores == 0):
			self._print_output('no_scores')
		else:
			for x, y in zip(self.df_paths,self.ind_scores):
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
			self._print_output('pass_on')
			self._outlet(1, [str(x) for x in self.df_paths])

	def bang_2(self):
		"""
		Check to see how many DataFrames exist, i.e. how many different scores
		were indexed. The number output can be used to select and individual 
		score for querying.
		"""
		try:
			self._outlet(2, len(self.ind_scores))
		except:
			self._print_output('no_scores')

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
		for x, y in zip(self.df_paths,self.ind_scores):
			
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
			'mto_parsed':'\nThe scores were thawed and parsed with music21.',
			'vis_parsed':'\nThe scores have been indexed with VIS.',
			'no_scores':'\nPlease load music21 streams first.',
			'pass_on':'\nThe note-rest-indexed DataFrames were passed on.',
			'nri_fail':'\nThe NoteRestIndexer failed.',
			'music21_fail':'\nMusic21 failed to unthaw the music21 streams.'
		}

		print(messages[print_what])

# ----- END NoteRestIndexer.py --------------------------------------- #
