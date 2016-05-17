# -*- coding: utf-8 -*-
"""
ConcatenatePieces.py
====================

Concatenates pandas DataFrames.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 05.16.2016

"""

import sys, os, music21, pyext
from collections import Counter

try:
	print("ConcatenatePieces.py was loaded.")
except:
	print("Loading ConcatenatePieces.py failed.")


class ConcatCompositions(pyext._class):
	"""
	Processes multiple DataFrames of the the same type into one large 
	DataFrame. 

	ConcatCompositions Class
	------------------------

	Adds multiple DataFrames into a singular DataFrame.

	Inlets:

	1. Takes paths to pickled DataFrames for concatenation.

	Outlets:
	
	1. The first outlet outputs the path to the concatenated DataFrame.
	
	"""

	def __init__(self, arg):
		super(ConcatCompositions, self).__init__()
		self.arg = arg
		

# ----- END ConcatenatePieces.py ------------------------------------- #
