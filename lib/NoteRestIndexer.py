# -*- coding: utf-8 -*-
"""
NoteRestIndexer.py
==================

A Python object to make the results of the NoteRestIndexer from the VIS
framework available to Pd.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 04.15.2016

"""

import sys, os, music21, pyext
from vis.analyzers.indexers import noterest

try:
    print("{} loaded.".format(sys.argv))
    print("Using Python {}.{}.{}.".format(
    	sys.version_info[0],
    	sys.version_info[1],
    	sys.version_info[2]))
except:
	print("Failed")

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
	_inlets = 2
	_outlets = 2

	# Init function.
	def __init__(self,mto_scores=0,ind_scores=0,df_paths=0):
		"""
		Storing variables used in this class.
		"""
		self.mto_scores = mto_scores
		self.ind_scores = ind_scores
		self.df_paths = df_paths
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
			

			local_msg = (self.mto_parsed + ": \n" + 
				str([str(x) for x in unthawed]))
			self._outlet(2, local_msg)

			for x in unthawed:
				print(x.metadata.all())

			try:

				self.ind_scores = [noterest.NoteRestIndexer(i).run()
					for i in unthawed]

				self.df_paths = []

				for i in range(len(self.ind_scores)):
					
					# Build the path names, and save them into a list variable.
					self.df_paths.append(
						os.path.dirname(os.path.realpath(__file__)) + 
						'/data/frames/' + str(i) + '.csv')

					# Save the dataframes as csv file.
					self.ind_scores[i].to_csv(
						self.df_paths[i],
						#na_rep="--",
						encoding='utf-8')

				#self._outlet(2, self.vis_parsed)
				self.bang_2()
				self._outlet(1, [str(x) for x in self.df_paths])

			except:

				self._outlet(1, self.err_msg_2)

		except:

			self._outlet(1, self.err_msg_1)

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



# ----- END NoteRestIndexer.py --------------------------------------- #
