## VIS-for-Pd project library
Most library files will consist of Python class/Pd abstraction pairs. An object in the following description refers to such a pair. 
#### MultiFile.py/openfile.pd
With this pair a user can open multiple files at once, and pass these files on to any object that will read these files. Any file type is accepted. The object can also accept just one file, like Pd's _openpanel_ object.
#### SymbolicMusic.py/parse-symbolic-music.pd
The object accepts any symbolic music file types that music21 can process, converts them music21 score streams, and pickles these streams for later use. Multiple files at once, or just one file can be processed.
#### NoteRestIndexer.py/note-rest-indexer.pd
The object takes any pickled music21 score streams, places these into pandas DataFrames with the VIS-Framework, and stores the DataFrames for quick recall. Any number of pickled music21 score streams, or just one can be used.

