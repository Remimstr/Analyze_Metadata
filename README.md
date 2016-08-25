# Standardize_Metadata
A collection of tools to download, parse, and standardize sequence metadata from NCBI databases.<br />
Written by Remi Marchand between May 13, 2016 and August 26, 2016.

## Scope
This collection of tools, by default, manipulates data from the Sequence Read Archive (SRA) database.<br />
The database can be found here: http://www.ncbi.nlm.nih.gov/sra

## Usage

### metadata.py
Main program that queries and downloads xml files based on organism name and date.<br />
**Usage:** metadata.py options (run python metadata.py -h to see options)<br />
**Download in Bulk:** bash download.sh organism start_date end_date<br />

### Standard_Tools/standardize.py
Main program that standardizes relevant columns from input csv files.<br />
**Usage:** standardize.py csv_files<br />

## Installation

### You may need to install the following modules
- lxml (install via pip as: python -m pip install lxml)<br />
- Levenshtein (install from: https://pypi.python.org/pypi/python-Levenshtein/0.12.0)<br />

### Add to the python path
- If on a Mac: export PYTHONPATH="${PYTHONPATH}:Path_to_Standardize_Metadata"<br />
