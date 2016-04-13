# -*- coding: utf-8 -*-
"""
# ----- MultiFile.py ------------------------------------------------- #

A Python object to capture multiple files.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 04.12.2016

Inlets:

1) When a bang is supplied, a file chooser dialog window appears to 
   select one or multiple files.

Outlets:

1) A list of file paths is sent through this outlet

# -------------------------------------------------------------------- #
"""

import sys, pyext, Tkinter, tkFileDialog

try:
    print("{} loaded.".format(sys.argv))
    print("Using Python {}.{}.{}.".format(
    	sys.version_info[0],
    	sys.version_info[1],
    	sys.version_info[2]))

except:
	print("Failed to load.")

class ReadFiles(pyext._class):
	"""
	Class to read multiple files into a list.
	"""
	_inlets = 1
	_outlets = 1

	
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
			le_machine = Tkinter.Tk()
			collected_files = tkFileDialog.askopenfilenames(parent=le_machine,
				title='Choose a symbolic music file')
			le_machine.withdraw()
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
		self._outlet(1, self.status_pass)

	def _msg_fail(self):
		"""
		Message provided to user if files were not successully added to 
		a list.
		"""
		self._outlet(1, self.status_fail)

# ----- END MultiFile.py --------------------------------------------- #