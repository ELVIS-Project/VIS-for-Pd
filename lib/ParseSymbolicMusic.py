# -*- coding: utf-8 -*-
"""
# ----- ParseSymbolicMusic.py ----------------------------------------- #

The ParseSymbolicMusic module takes a symbolic music file for it's 
input, parses that input with music21, and outputs an array of music21
"streams".

Author:		Reiner Kramer	
Email:		reiner@music.org
Updated:	04.13.2016

# -------------------------------------------------------------------- #
"""

import sys, os, music21, pyext

try:
        print("{} loaded.".format(sys.argv))
        print("Using Python {}.{}.{}.".format(
                sys.version_info[0],
                sys.version_info[1],
                sys.version_info[2]))
except:
		print("Failed")
        
class Parse(pyext._class):

	"""
	Parses a score through music21.

	Inlets:

	1. Default inlet: Documentation string, reload, etc.
	2. Takes a list of file paths (file names + paths).
	3. Bang to recall whether or not streams already exist.

	Outlets:

	1. List of music21 streams.
	2. Returns a debug message, if so desired.
	3. Default outlet (does nothing?). 

	"""

	# How many inlets and outlets.
	_inlets = 1
	_outlets = 2

	# Init function.
	def __init__(self,mto_score_list=0,mto_frozen_list=0):
		"""
		Init function for storing variables used in this class.
		"""
		self.mto_score_list = mto_score_list
		self.mto_frozen_list = mto_frozen_list

	# Handling inlets.
	def _anything_1(self,*symbolic_score_list):
		"""
		Parses a score in music21.
		"""
		try:

			self.mto_score_list = [music21.converter.parse(str(x)) 
				for x in symbolic_score_list]

			#self.mto_frozen_list = []
			
			directory = os.path.dirname(os.path.realpath(__file__)) + '/data/'

			frozen_list = []
			for i in range(len(self.mto_score_list)):
				frozen_list.append(music21.converter.freeze(self.mto_score_list[i],fmt='pickle',fp=(directory + str(i) + '.pgz')))

			self._outlet(2, frozen_list)

		except:

			self._outlet(2, "Nope.")

	def bang_1(self):
		"""
		Bang to check of there are already parsed music21 scores.
		"""
		if(self.mto_score_list == 0):
			print("There are currently no music21 score streams present.")
		else:
			# print(self.mto_score_list)
			pathy = '/Users/reiner/Documents/MusicAnalyses/VIS-for-Pd/lib/data/'
			filename = music21.converter.freeze(self.mto_score_list[0],
				fmt='pickle',
				fp=(pathy+'mango.pgz'))

			# print(filename)

			musky = music21.converter.thaw(filename)

			self._outlet(2, str(musky))

# ----- END ParseSymbolicMusic.py ------------------------------------ #
