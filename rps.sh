#!/bin/bash

# Find all files and directories containing '{{cookiecutter.'
find . -name '*{{cookiecutter.*' | while read filename; do
    # Replace '{{cookiecutter.' with '{{' in the filename
    new_filename=$(echo "$filename" | sed 's/{{cookiecutter\./{{/g')
    # Rename the file
    mv "$filename" "$new_filename"
done