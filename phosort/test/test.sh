#!/bin/sh

# Begin test
clear

# Prepare test directory
echo "Setup test environment..."
mkdir -p bin
cp -R * bin
echo "Setup complete"

# Run test
echo "Run sort..."
python phosort.py bin -r -s -d -c
echo "Sort complete"

# Clean up
rm test -rf
echo "Clean-up complete"

