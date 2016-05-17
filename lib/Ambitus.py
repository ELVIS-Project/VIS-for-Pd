# -*- coding: utf-8 -*-
"""
Ambitus.py
==========

Get the ambitus of a music21 stream without a pitch count.

Author: Reiner Kramer	
Email: reiner@music.org
Updated: 05.16.2016

"""

import sys, os, music21, pyext

try:
	print("Ambitus.py was loaded.")
except:
	print("Ambitus.py failed.")

class Find(pyext._class):
	"""
	Finds the ambitus of a voice, or piece, from a music21 stream.

	AmbitusFind Class:

	1. Inlet: Takes music21 stream(s).
	2. Outlet: Outputs ambiti.

	"""

	_inlets = 3
	_outlets = 1

	def __init__(self,
		mto_scores=0,
		meta=0,
		ambiti=0,
		pitch_id='nameWithOctave',
		print_pd_win='True'):
		"""
		Init function.
		"""
		self.mto_scores = mto_scores
		self.meta = meta
		self.ambiti = ambiti
		self.pitch_id = pitch_id
		self.print_pd_win = print_pd_win

	def _anything_1(self,*pickeled_scores):
		"""
		Loops through pickeled scores and creates range reports.
		"""

		if(pickeled_scores == 0):

			print(self._msg_missing_scores())

		else:

			try:

				pickeled = [str(x) for x in pickeled_scores]

				self.mto_scores = [music21.converter.thaw(x) 
					for x in pickeled]
				
				self.meta = [(x.metadata.composer + ": " + x.metadata.title) 
					for x in self.mto_scores]

				self.ambiti = self._calc_ambiti(self.mto_scores)
				
				if(self.print_pd_win == 'True'):
					self._print_ambiti(self.ambiti,self.meta)
				else:
					self._send_ambiti(self.ambiti,self.meta)

			except Exception as e:

				print(e)

	def _anything_2(self, pitch_identification):
		"""
		Specify what type of pitch names to display. Options are music21 
		options: pitchClass, name, nameWithOctave, midi.
		"""
		self.pitch_id = str(pitch_identification)
		self.ambiti = self._calc_ambiti(self.mto_scores)
		self._print_ambiti(self.ambiti,self.meta)

	def _anything_3(self, print_pd_win):
		"""
		Option to print to Pd window or to send results to objects 
		outlet. If set to 'True' then printing to the Pd Window is 
		enabled, if set to 'False' the results are sent to the outlet, 
		which then can be printed with a Print object.
		"""
		self.print_pd_win = str(print_pd_win)

	def _calc_ambiti(self, scores):
		"""
		Calculates the ambiti of scores.
		"""

		ambana = music21.analysis.discrete.Ambitus()

		ambiti = [[getattr(x, self.pitch_id) 
			for x in ambana.getPitchSpan(y)] 
			for y in scores]

		return ambiti	

	def _print_ambiti(self, ambiti, meta):
		"""
		Prints ambiti to the Pd window.
		"""
		for x, z in zip(ambiti, meta):
			print("\n{0} \n".format(z) + len(z) * "-")
			print("Ambitus: {0} => {1}".format(str(x[0]),str(x[1])))

	def _send_ambiti(self, ambiti, meta):
		"""
		Sends the ambiti to the outlet
		"""
		out_package = ["\n{0}\nAmbitus: {1} => {2}\n".format(str(z), 
			str(x[0]), str(x[1])) for x, z in zip(ambiti, meta)]
		self._outlet(1, out_package)

	def _msg_missing_scores(self):
		"""
		Method to indicate that no music21 streams have been loaded.
		"""
		return "Please load music21 streams first."


# ----- END Ambitus.py ----------------------------------------------- #