#!/usr/bin/python3
#
# Copyright 2010 Anthony Campbell (anthonycampbell.co.uk)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Photo and Video sort script

Simple script which aides in the maintainence of a large photo / video
collection. Sort output structure:

    /YYYY/Original Folder Names/File
    
Author:  Anthony Campbell (anthonycampbell.co.uk)
Version: 0.0.1
Date:    22nd August, 2010
"""

# Required imports
import sys, os, fnmatch, re

# Supported help flags
_helpArgs = ("-help", "--help", "-?", "--?")
_help = """
    __file__ [directory] [option]

    Simple script which attempts to sort photo and video files in the
    specified directory. Output produces the following format:

        /YYYY/Original Folder Names/File

    Directory:
        Absolute or relative path to the directory being sorted. If this
        argument is not provided the current directory will be used.

    Options:
        -s Option to replace directory and file name spaces with the "-"
        character.

        -r Option to rename all sorted files to reflect the parent directory
        name and creation date.

        -i Option to only sort images.

        --help -help -? --? Option to display this text.
"""
_help = _help.replace("__file__", __file__)

# Supported flags
_supportedOptions = ("-s", "-r", "-i") + _helpArgs

# Config
_directory = os.getcwd()
_replaceSpaces = False
_renameFiles = False
_imageOnly = False

# Check for any options
for _arg in sys.argv:
    if _arg not in _supportedOptions and not _arg == __file__ and _directory == os.getcwd():
        # Get first valid directory argument
        _directory = _arg

        # Validate
        if not os.path.exists(_directory):
            raise IOError("Provided directory does not exist!")
        if not os.path.isdir(_directory):
            raise IOError("Provided argument is not a directory!")
    if _arg == "-s":
        print ("Need to replace spaces with -")
        _replaceSpaces = True
    if _arg == "-r":
        print ("Need to rename files during sort")
        _renameFiles = True
    if _arg == "-i":
        print ("Need to sort images only")
        _imageOnly = True
    if _arg in _helpArgs:
        print (_help)
        exit(0)

def print_title(_title):
    """
    Simple function print titles to the console in a consistent way.

    Args:
        _title the title to print to the console.
    """
    print (("\n" + ("=" * len(_title))))
    print (_title)
    print (("=" * len(_title)) + "\n")

# Declare Steps
_beginMessage = "BEGIN phosort"
_endMessage = "END phosort"

# Begin
print_title(_beginMessage)

print ("Current working directory:", _directory)
print ("Replace spaces: ", _replaceSpaces)
print ("Rename files:   ", _renameFiles)
print ("Image only sort:", _imageOnly, "\n")

# Match supported files
_directoryListing = os.listdir(_directory)
print (_directoryListing)

#if fnmatch.fnmatch(file, '*.txt'

#_directoryListing = glob.glob("(.{1,2})?(*.jpg)?")
#_directoryListing = glob.glob(".|*.[jpg|JPG|JPEG|jpeg]")

print (_directoryListing)

# End
print_title(_endMessage)


