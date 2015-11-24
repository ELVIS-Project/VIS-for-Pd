# - *- coding: utf-8 -*-
#! /usr/local/bin python

import sys, os
import music21 as mto

# Pd window message that file has properly loaded.
print("{} loaded.".format(os.path.basename(__file__)))

# Pd window message that music21 module has properly loaded.
try:
	print("{} loaded via {}.".format(mto, sys.argv))
except:
	print 

def loadbang():
	print "loaded."

def ps_name_to_midi(note_arg):
	"""
	Translating a not name with it's octave designation to a midi value
	(i.e. truncating a note).
	>>> ps_name_to_midi('C#4')
	61
	"""
	midi_note = mto.pitch.Pitch(str(note_arg))
	return midi_note.midi

def midi_to_pc_name(midi_arg):
	"""
	Convert a midi number to a pitch name. E.g.: 61 => C#.
	>>> midi_to_pc_name(61)
	'C#'
	"""
	pc_name = mto.pitch.Pitch(int(midi_arg))
	return pc_name.name

def midi_to_ps_name(midi_arg):
	"""
	Convert a midi number to a pitch space name. E.g.: 61 => C#4.
	>>> midi_to_ps_name(61)
	'C#4'
	"""
	ps_name = mto.pitch.Pitch(int(midi_arg))
	return ps_name.nameWithOctave

def bang_test(bang='bang'):
	"""
	Receive and evaluate a bang.
	>>> bang_test('bang')
	'bang'
	"""
	return bang

def main():
	"""
	Using main only for doctest.
	"""
	import doctest
	doctest.testmod()

if __name__ == '__main__':
	main()
