Copyright 2010 Anthony Campbell (anthonycampbell.co.uk)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific
language governing permissions and limitations under the License.

--------------------------------------
phosort
--------------------------------------

Simple script to sort a directory of photos and videos. Designed
to break down a directory into yearly creation date sub directories.
Also rename files to provide a more consistent and readable listing.

Please look at the CHANGES file in each project to see what has
changed since the last tag.

------------------------
Dependencies:
------------------------

    * hachoir-core-1.3.3
    * hachoir-parser-1.3.4
    * hachoir-metadata-1.3.3

These packages are available from the ./dependencies directory.
Simply unzip and run the "python setup.py install" command as root
on all three libraries.

------------------------
PIP install:
------------------------

    pip install phosort

------------------------
Manual install:
------------------------

Download the provided source and execute it using the following
command:

    python setup.py install

------------------------
Usage:
------------------------

    python phosort.py [directory] [option]

------------------------
Contribute:
------------------------

If you wish to contribute to the project you can find the
latest source code on GitHub:

    http://wiki.github.com/acampbell3000/python-scripts/

------------------------
Further information:
------------------------

phosort is now also available on PyPi Package Index (PyPI) (aka, the "Cheeseshop"):

    http://pypi.python.org/pypi/phosort

------------------------
Special thanks:
------------------------

To Alex Elder (alexelder.co.uk) for his numerous fixes and improvements. Cheers dude!

