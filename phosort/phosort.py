#!/usr/bin/python
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
collection. Sorts the provided directory into the following structure:

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
import time
import shutil

# Hachoir metdata dependencies
import hachoir_core.config as hachoir_config
from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from hachoir_metadata import extractMetadata

# Supported help flags
_help_args = ("-help", "--help", "-?", "--?")
_help = """
    __file__ [directory] [option]

    Simple script which attempts to sort photo and video files in the
    specified directory. Output produces the following format:

        /YYYY/Original Folder Names/File [timestamp]

    Directory:
        Absolute or relative path to the directory being sorted. If this
        argument is not provided the current directory will be used.

    Options:
        -s Option to replace file name spaces with the "-" character.

        -d Option to replace directory name spaces with the "-" character.

        -r Option to rename all sorted files to reflect the parent directory
        name and creation date.

        -i Option to only sort images.

        -c Copy the files to the new sorted location instead of a move.

        -t, -! Option to only simulate and output the sort and to not persist any
        changes. Allows changes to be viewed before persisting them.

        --help -help -? --? Option to display this text.
"""
_help = _help.replace("__file__", __file__)

# Supported flags
_supported_options = ("-s", "-r", "-d", "-i", "-c", "-t", "-!") + _help_args

# Supported file types regex
_supported_images_regex = ".+\.(jpe?g)"
_supported_movies_regex = ".+\.(avi|mov)"

# Report
_sorted_years = []

# Config
_directory = os.getcwd()
_rename_files = False
_replace_file_spaces = False
_replace_directory_spaces = False
_image_only = False
_file_copy = False
_simulate_only = False

def output(*_messages):
    """
    Simple function to print the provided message in a consistent
    way between python2 and python3.

    Args:
        _message the message to print.
    """
    # Initialise result
    _output = ""

    # Concatenate tuple into single string
    for _message in _messages:
        _output += str(_message) + " "
    print (_output)


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
        _replace_file_spaces = True
    if _arg == "-d":
        _replace_directory_spaces = True
    if _arg == "-r":
        _rename_files = True
    if _arg == "-c":
        _file_copy = True
    if _arg == "-i":
        _image_only = True
    if _arg == "-t" or _arg == "-!":
        _simulate_only = True
    if _arg in _help_args:
        output (_help)
        exit(0)


def print_title(_title):
    """
    Simple function print titles to the console in a consistent way.

    Args:
        _title the title to print to the console.
    """
    output (("\n" + ("=" * len(_title))))
    output (_title)
    output (("=" * len(_title)) + "\n")


def get_creation_date(_path):
    """
    Simple function to retrieve the creation date from the file's metdata

    Args:
        _path the full path to the file.
    """
    # Initialise result
    _creation_date = None

    # Using the hachoir metadata library retrieve file metadata    
    hachoir_config.quiet = True
    try:
        parser = createParser(unicodeFilename(_path), _path)
        if parser:
            metadata = extractMetadata(parser)
            if metadata:
                _creation_date = metadata.get("creation_date")
    except Exception:
        pass

    # Return result
    return _creation_date


def rename_file(_filename, _date):
    """
    Simple function to re-name the provided file name to append a time
    stamp.

    Args:
        _filename the file name to re-name.
        _date the date to append to the file name.
    """
    # Initialise result
    _new_filename = _filename
    _timestamp = "-"

    # Generate timestamp
    if _date:
        _day = str(_date.day)
        _month = str(_date.month)
        _year = str(_date.year)

        if len(_day) < 2:
            _day = "0" + _day
        if len(_month) < 2:
            _month = "0" + _month

        _timestamp += _year + "-" + _month + "-" + _day

    # Does timestamp already exist
    _exist = re.search(r"\(([0-9\-\s]+|.*Jan.*|.*Feb.*|.*Mar.*|.*Apr.*|.*May.*|.*Jun.*|.*Jul.*|.*Aug.*|.*Sep.*|.*Oct.*|.*Nov.*|.*Dec.*)\)", _new_filename)
    if _exist and not _exist.lastindex == None:
        # If replacing spaces them we should remove brackets
        if _replace_file_spaces:
            _old_timestamp = _new_filename[_exist.start(0):_exist.end(0)]
            _new_timestamp = _old_timestamp.replace("(", "").replace(")", "")
            _new_filename = _new_filename.replace(_old_timestamp, _new_timestamp).lower()
    else:
        # Find image extension
        _match = re.search(_supported_images_regex, _new_filename, flags=re.IGNORECASE)
        if _match and not _match.lastindex == None:
            _start = _new_filename[:_match.start(1)]
            _extension = _new_filename[_match.start(1):_match.end(1)]
            _end = _new_filename[_match.end(1):]
            _new_filename = _start + _timestamp + _extension + _end

        else:
            # Find movie extension
            _match = re.search(_supported_movies_regex, _new_filename, flags=re.IGNORECASE)
            if _match and not _match.lastindex == None:
                _start = _new_filename[:_match.start(1)]
                _extension = _new_filename[_match.start(1):_match.end(1)]
                _end = _new_filename[_match.end(1):]
                _new_filename = _start + _timestamp + _extension + _end

    return _new_filename


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
        if re.match(_supported_images_regex, _file, flags=re.IGNORECASE):
            _matched_files += [_file]
        if not _image_only and re.match(_supported_movies_regex, _file, flags=re.IGNORECASE):
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
    # Initialise results
    global _sorted_years
    _count = 0

    # Begin file sort
    for _file in _files_to_sort:
        # Get creation date
        _date = get_creation_date(_file)
        if not _date:
            _creation_date = os.path.getctime(_file)
            _date = datetime.date.fromtimestamp(_creation_date)

        _year = str(_date.year)

        # Update record
        if _year not in _sorted_years:
            _sorted_years += [_year]

        # Now move into year directory
        _new_path = os.path.normpath(os.path.join(_year, _file))
        _parents = _new_path[:_new_path.rfind("/")]

        # Update file name if required
        if _rename_files:
            _filename = os.path.basename(_new_path)
            _new_filename = rename_file(_filename, _date)
            _new_path = _new_path.replace(_filename, _new_filename)

        # Replace file spaces if required
        if _replace_file_spaces:
            _filename = os.path.basename(_new_path)
            _new_filename = _filename.replace(", ", "-").replace(" ", "-")
            _new_path = _new_path.replace(_filename, _new_filename)

        # Replace directory spaces if required
        if _replace_directory_spaces:
            _new_parents = _parents.replace(", ", "-").replace(" ", "-")
            _new_path = _new_path.replace(_parents, _new_parents)
            _parents = _new_parents

        if not os.path.exists(_new_path):
            # Create parents
            if not os.path.exists(_parents) and not _simulate_only:
                os.makedirs(_parents)

            # Move / Copy
            if not _simulate_only:
                if _file_copy:
                    output (_file, "-+->", _new_path)
                    shutil.copy2(_file, _new_path)
                else:
                    output (_file, "--->", _new_path)
                    shutil.move(_file, _new_path)
                _count += 1
            else:
                output (_file, "-!->", _new_path)
    
    # Return result
    return _count

# Declare steps
_begin_message = "BEGIN phosort"
_end_message = "END phosort"

# Begin
print_title(_begin_message)

output ("Sort directory:           ", _directory)
output ("Replace file spaces:      ", _replace_file_spaces)
output ("Replace directory spaces: ", _replace_directory_spaces)
output ("Rename files:             ", _rename_files)
output ("Image only sort:          ", _image_only)
output ("File copy:                ", _file_copy)
output ("Simulate only:            ", _simulate_only)

# Change directory to search root
os.chdir(_directory)
_start = time.time()

# Cleaner exit for a keyboard interrupt
try:
    # Match supported files
    output ("\nBegin search...")
    _matched_files = file_search(".")
    output ("Number of files found:", len(_matched_files))

    # Begin sort
    output ("\nBegin sort...")
    _total = file_sort(_matched_files)

    if _file_copy:
        output ("\nNumber of files copied:", _total)
    else:
        output ("\nNumber of files moved:", _total)
except KeyboardInterrupt:
    output ("KeyboardInterrupt:", "Stopping seach...")

# Prepare year report
_sorted_years.sort()
_sorted_years = ",".join(_sorted_years).replace(",", ", ")
if _simulate_only:
    output ("Years found:", _sorted_years)
else:
    output ("Years sorted:", _sorted_years)

# End time
_elapsed = (time.time() - _start)
output ("Time elapsed:", _elapsed)

# End
print_title(_end_message)

