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
import sys
import os
import re
import datetime
import shutil

# Supported help flags
_help_args = ("-help", "--help", "-?", "--?")
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

        -d Option to only simulate and output the sort and to not persist any
        changes. Allows changes to be viewed before persisting them.

        --help -help -? --? Option to display this text.
"""
_help = _help.replace("__file__", __file__)

# Supported flags
_supported_options = ("-s", "-r", "-i", "-d") + _help_args

# Config
_directory = os.getcwd()
_replace_spaces = False
_rename_files = False
_image_only = False
_simulate_only = False

# Check for any options
for _arg in sys.argv:
    if _arg not in _supported_options and not _arg == __file__ and _directory == os.getcwd():
        # Get first valid directory argument
        _directory = _arg

        # Validate
        if not os.path.exists(_directory):
            raise IOError("Provided directory does not exist!")
        if not os.path.isdir(_directory):
            raise IOError("Provided argument is not a directory!")
    if _arg == "-s":
        print ("Need to replace spaces with -")
        _replace_spaces = True
    if _arg == "-r":
        print ("Need to rename files during sort")
        _rename_files = True
    if _arg == "-i":
        print ("Need to sort images only")
        _image_only = True
    if _arg == "-d":
        _simulate_only = True
    if _arg in _help_args:
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

def file_search(_directory):
    """
    Search for the supported file types in the provided directory. This
    function is recursive and will also search sub-directories.

    Args:
        _directory the current directory to search.
        _root the root directory of the search.
    """
    # Initialise result
    _matched_files = []

    # Get directory listing
    _directory_listing = os.listdir(_directory)

    # Begin search
    for _file in _directory_listing:
        # Maintain relative path
        _file = os.path.join(_directory, _file)

        # Match supported files
        if re.match(".+(.jpg|.JPG|.jpeg|.JPEG)", _file):
            _matched_files += [_file]
        if not _image_only and re.match(".+(.avi|.AVI|.mov|.MOV)", _file):
            _matched_files += [_file]

        # Search any sub-directories
        if os.path.isdir(_file):
            _matched_files += file_search(_file)
    return _matched_files

def file_sort(_files_to_sort):
    """
    Sort the provided file list to take into account creation date.

    Args:
        _files_to_sort the list of files to sort.
    """
    # Initialise result
    _count = 0

    # Begin file sort
    for _file in _files_to_sort:
        # Get creation date
        _creation_date = os.path.getctime(_file)
        _date = datetime.date.fromtimestamp(_creation_date)
        _year = str(_date.year)

        # Now move into year directory
        _new_path = os.path.normpath(os.path.join(_year, _file))
        _parents = _new_path[:_new_path.rfind("/")]

        # Replace spaces if required
        if _replace_spaces:
            _new_path.replace(" ", "-")
            _parents.replace(" ", "-")

        if not os.path.exists(_new_path):
            # Create parents
            if not os.path.exists(_parents) and not _simulate_only:
                os.makedirs(_parents)

            # Move 
            print (_file, "-->", _new_path)
            if not _simulate_only:
                shutil.move(_file, _new_path)
                _count += 1
    
    # Return result
    return _count

# Declare steps
_begin_message = "BEGIN phosort"
_end_message = "END phosort"

# Begin
print_title(_begin_message)

print ("Directory:", _directory)
print ("Replace spaces: ", _replace_spaces)
print ("Rename files:   ", _rename_files)
print ("Image only sort:", _image_only)
print ("Simulate only:  ", _simulate_only)

# Change directory to search root
os.chdir(_directory)

# Match supported files
print ("\nBegin search...")
_matched_files = file_search(".")
print ("Number of files found:", len(_matched_files))

# Begin sort
print ("\nBegin sort...")
_total = file_sort(_matched_files)
print ("Number of files moved:", _total)

# End
print_title(_end_message)

