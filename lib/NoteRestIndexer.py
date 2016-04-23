# -*- coding: utf-8 -*-
"""
NoteRestIndexer.py
==================

A Python object to make the results of the NoteRestIndexer from the VIS
framework available to Pd.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 04.22.2016

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
		slice_end=5):
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
		# Messages
		self.err_msg_1 = ("There wasn't enough heat to thaw the frozen " + 
			"music21 object.")
		self.err_msg_2 = "The NoteRestIndexer failed."
		self.mto_parsed = "The scores were thawed and parsed with music21."
		self.vis_parsed = "The scores have been indexed with VIS."

	def _anything_1(self,*pickled_scores):
		"""
		Parses a list of pickeled music21 scores, and indexes the scores with 
		the vis-framework's NoteRestIndexer into pandas DataFrames.
		"""
		try:

			pickled = [str(x) for x in pickled_scores]
			unthawed = [music21.converter.thaw(pickled[i]) 
				for i in range(len(pickled))]

			'''	
			# Debug:
			local_msg = (self.mto_parsed + ": \n" + 
				str([str(x) for x in unthawed]))
			print(local_msg)
			'''

			meta = [(x.metadata.composer + "_" + 
				x.metadata.title).replace(" ", "-") 
				for x in unthawed]

			'''
			# Debug
			for y in meta:
				print y
			'''

			try:

				self.ind_scores = [noterest.NoteRestIndexer(i).run()
					for i in unthawed]

				self.df_paths = []

				for i in range(len(self.ind_scores)):
					
					# Build the path names, and save them into a list variable.
					self.df_paths.append(
						os.path.dirname(os.path.realpath(__file__)) + 
						'/data/frames/noterest/' + meta[i] + '.pkl')

					# Save the dataframes as pickle(d) files.
					self.ind_scores[i].to_pickle(self.df_paths[i])

				#self._outlet(2, self.vis_parsed)
				self.bang_2()
				self._outlet(1, [str(x) for x in self.df_paths])
				'''
				for x in self.df_paths:
					print str(x)
				'''
				print(self.mto_parsed)

				for x, y in zip(self.df_paths,self.ind_scores):
					comp_name = self._generate_name(x)
					print("\n" + comp_name)
					print(len(comp_name) * "-")
					print(y.head(5).to_csv(
						sep='\t',
						na_rep='^'))

			except:

				self._outlet(1, self.err_msg_2)

		except:

			self._outlet(1, self.err_msg_1)

	def _anything_2(self,events):
		"""
		Determines how many events are to be shown.
		"""
		if(self.ind_scores == 0):
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
		if(self.ind_scores == 0):
			self._msg_missing_score()
		else:
			self.direction = str(direction)
			self._heads_or_tails()

	def _anything_4(self,slice_start,slice_end):
		"""
		Picks a slice from a given DataFrame.
		"""
		if(self.ind_scores == 0):
			self._msg_missing_score()
		else:
			for x in self.ind_scores:
				print(x.iloc[slice_start:slice_end].to_csv(
					sep='\t',
					na_rep='^'))

	def bang_1(self):
		"""
		Checks wether or not a DataFrame exists or should be loaded.
		"""
		if(self.df_paths == 0):
			self._outlet(1, self._msg_missing_scores())
		
		else:
			# self._outlet(1, "DataFrames exist.")
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
			self._outlet(2, self._msg_missing_scores())

	def _msg_missing_scores(self):
		"""
		Method to indicate that no DataFrames have been loaded.
		"""
		return "Please load (a) music21 stream(s) first."

	def _generate_name(self,path):
		"""
		Private method to generate a human readable name of a composition from
		it path.
		"""
		file_name = os.path.split(path)
		file_extr = os.path.splitext(file_name[1])
		comp_name = str(file_extr[0]).replace("-"," ").replace("_",": ")

		return comp_name

	# Local methods: complying with DRY.
	def _heads_or_tails(self):
		"""
		Helper method to determine whether to count from the beginning
		or from the end of the DataFrame.
		"""
		if(self.direction == 'end'):
			for x in self.ind_scores:
				print(x.tail(self.events).to_csv(
						sep='\t',
						na_rep='^'))
			#self._outlet(1,self.ind_score.tail(self.events).to_csv())
		else:
			for x in self.ind_scores:
				print(x.head(self.events).to_csv(
						sep='\t',
						na_rep='^'))
			#self._outlet(1,self.ind_score.head(self.events).to_csv())



# ----- END NoteRestIndexer.py --------------------------------------- #
