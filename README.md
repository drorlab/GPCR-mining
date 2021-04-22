# GPCR-mining
Functions to scrape GPCR data from the web.

## Installation

    git pull https://github.com/drorlab/GPCR-mining
    cd GPCR-mining
    pip install -e .

## Get a sequence with numbering from the GPCRdb

The GPCRdb provides a comprehensive overview for the sequence of a GPCR, including a convenient numbering scheme, based on Ballesteros-Weinstein numbering.
Looking up a large number of residues or including the conversion for a specific receptor into an automated workflow can become tedious.

To save such a sequence in a more easily usable CSV file, run

    python -m gpcrmining.gpcrdb -n <GPCR_NAME> -d <DIRECTORY>

with "<GPCR_NAME>" being the name of the GPCR as used in the corresponding GPCRmd URL and "<DIRECTORY>" is the directory where the data should be saved.

For example,

    python -m gpcrmining.gpcrdb -n adrb1_human -d .

writes the file 'gpcrdb-residues_adrb1_human.csv' into the current directory


