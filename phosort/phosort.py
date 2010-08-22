######################################################
#                                                    #
# Photo and Video Sort script                        #
#                                                    #
# Simple scripts which aides in the maintainence     #
# of a large photo / video collection. Sort output   #
# structure:                                         #
#                                                    #
# /YYYY/Original Folder Names/File                   #
#                                                    #
# Anthony Campbell (anthonycampbell.co.uk)           #
# Version: 0.0.1                                     #
# Date: 22nd August, 2010                            #
#                                                    #
######################################################

# Required imports
import sys, os, re

# Supported help flags
_helpArgs = ("-help", "--help", "-?", "--?")
_help = """
    __file__ [option]

    hi
"""
_help = _help.replace("__file__", __file__)

# Modes
_replaceSpaces = False
_renameFiles = False
_imageOnly = False

# Check for any flags
for arg in sys.argv:
    if arg == "-s":
        print ("Need to replace spaces with -")
        _replaceSpaces = True
    if arg == "-r":
        print ("Need to rename files during sort")
        _renameFiles = True
    if arg == "-i":
        print ("Need to sort images only")
        _imageOnly = True
    if arg in _helpArgs:
        print (_help)
        exit(0)

# Begin
_beginMessage = "BEGIN phosort"
print (_beginMessage)
print (("=" * len(_beginMessage)), "\n")
print ("Current working directory:", os.getcwd())
print ("Replace directory / file name spaces:", _replaceSpaces)
print ("Rename files:", _renameFiles)
print ("Image only sort:", _imageOnly, "\n")



