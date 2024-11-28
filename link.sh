#!/bin/bash

# Remove existing symlink if it exists
rm -f RayCommonPy

# Create symbolic link
ln -s ../RayCommonPy RayCommonPy
