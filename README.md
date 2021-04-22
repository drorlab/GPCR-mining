# GPCR-mining
Functions to scrape GPCR data from the web.

## Installation

    git clone https://github.com/drorlab/GPCR-mining
    cd GPCR-mining
    pip install -e .

## Get a sequence with numbering from the GPCRdb

The [__GPCRdb__](https://gpcrdb.org) provides a comprehensive overview for the sequence of a GPCR, including a convenient numbering scheme, based on Ballesteros-Weinstein numbering.
Looking up a large number of residues or including the conversion for a specific receptor into an automated workflow can become tedious.

To save such a sequence in a more easily usable CSV file, run

    python -m gpcrmining.gpcrdb -n <GPCR_NAME> -d <DIR>

with "<GPCR_NAME>" being the name of the GPCR as used in the corresponding GPCRmd URL and "<DIR>" is the directory where the data should be saved (which is created if it does not exist).

For example,

    python -m gpcrmining.gpcrdb -n adrb1_human -d .

writes the file 'gpcrdb-residues_adrb1_human.csv' into the current directory


