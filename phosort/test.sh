#!/bin/sh

# Begin test
clear

# Prepare test directory
echo "Setup test environment..."
mkdir -p test
cp -R ./test-images/* test
echo "Setup complete"

# Run test
echo "Run sort..."
python phosort.py test -! -r -s -d -c
echo "Sort complete"

# Clean up
#rm test -rf
echo "Clean-up complete"

