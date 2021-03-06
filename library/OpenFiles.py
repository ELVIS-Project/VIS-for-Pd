# -*- coding: utf-8 -*-
"""
OpenFile.py
============

A Python object to capture multiple files.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 11.15.2016

Inlets:

1. When a bang is supplied, a file chooser dialog window appears to 
   select one or multiple files.

Outlets:

1. A list of file paths is sent through this outlet

# -------------------------------------------------------------------- #
"""

import sys, pyext, Tkinter, tkFileDialog

try:
	print("Multiple files read is enabled.")
except:
	print("Failed to load MultiFile.py.")

class ReadFiles(pyext._class):
	"""

	OpenFiles.py Module
	===================

	ReadFiles Class
	---------------
	
	Reads multiple files into a list.

	Inlets:

	1. Default inlet: Documentation string, reload, etc.
	2. A bang that opens a openfile window.

	Outlets:

	1. Returns list of files.
	2. Returns a debug message, if so desired.
	3. Default outlet.

	"""
	_inlets = 1
	_outlets = 2

	def __init__(self,the_files=0):
		"""
		Init function for the ReadFiles class.
		"""
		self.the_files = the_files
		self.status_pass = "Files were placed into a list."
		self.status_fail = "Files were not placed into a list."

	def bang_1(self):
		"""
		Opens a file chooser dialog window when a bang is passed to 
		method. The user can proceed to choose one or more files, which 
		are then passed to first outlet.
		"""
		try: 
			Tkinter.Tk().withdraw()
			# TODO: Dialogue window opens behind Pd patch, but should be forced
			#       to the front
			# le_machine.lift()
			# le_machine.focus_force()
			collected_files = tkFileDialog.askopenfilenames()
			self.the_files = collected_files
			self._outlet(1, self.the_files)
			self._msg_success()

		except:
			self._msg_fail()

	def _msg_success(self):
		"""
		Message provided to user if files have been successfully placed 
		into a list.
		"""
		self._outlet(2, self.status_pass)

	def _msg_fail(self):
		"""
		Message provided to user if files were not successully added to 
		a list.
		"""
		self._outlet(2, self.status_fail)

# ----- END OpenFiles.py --------------------------------------------- #