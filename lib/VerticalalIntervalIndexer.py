# -*- coding: utf-8 -*-
"""
VerticalIntervalIndexer.py
==========================

A Python object to to interpret a NoteRestIndexed DataFrame. A new DataFrame is
created to find vertical intervals in any given sounding simultaneity
line via the VIS-Framework.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 04.20.2016

"""

import sys, os, music21, pyext
from vis.analyzers.indexers import noterest, interval

try:
	print("VerticalIntervalIndexer.py was loaded.")
except:
	print("Loading VerticalIntervalIndexer.py failed.")

