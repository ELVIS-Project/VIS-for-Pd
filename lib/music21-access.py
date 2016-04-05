# -*- coding: utf-8 -*-
"""
music21-access.py demonstrates how to access the music21 library from within
pure data (Pd) by converting a string based pitch name to a midi pitch. String
based pitch names are formatted as follows: D#4 (D-Sharp), D-4 (D-Flat), D4
(D-natural)
"""
import sys
import music21 as mto

print("Script initialized.")

try:
	print "Script arguments: ", sys.argv
except:
	print 

def g_natural_to_midi():
	"""
	Print a G4 as a MIDI value.

	>>> g_natural_to_midi()
	67
	"""

	g_natural = mto.pitch.Pitch("G4")

	return g_natural.midi

def get_midi_pitch(note_arg):
	"""
	Getting a midi value from any pitch string e.g.: 'A4'.

	>>> get_midi_pitch('A4')
	69
	"""

	pitch_name = str(note_arg)
	a_note = mto.pitch.Pitch(pitch_name)

	return a_note.midi

if __name__ == "__main__":
    import doctest
    doctest.testmod()
