# GPCR-mining
Functions to scrape GPCR data from the web.

## Installation

    git clone https://github.com/drorlab/GPCR-mining
    cd GPCR-mining
    pip install -e .

## GPCRdb sequence numbering

The [__GPCRdb__](https://gpcrdb.org) provides a comprehensive overview for the sequence of a GPCR, including a convenient numbering scheme, based on Ballesteros-Weinstein numbering.
Looking up a large number of residues or including the conversion for a specific receptor into an automated workflow can become tedious.

### Obtain the entire sequence

To obtain such a sequence and to save it in a more easily usable CSV file, run

    python -m gpcrmining.gpcrdb -n GPCR_NAME -d DIR

with "GPCR_NAME" being the name of the GPCR as used in the corresponding GPCRmd URL and "DIR" is the directory where the data should be saved (which is created if it does not exist).

For example,

    python -m gpcrmining.gpcrdb -n adrb1_human -d data-gpcrmd

writes the file 'gpcrdb-residues_adrb1_human.csv' into the directory data-gpcrmd.

### Select specific residues and formats

You can select residues and print their information in various formats.
To select by the GPCRdb numbering, use the option '-id'. The residues have to be provided in the format X.Y with X the part of the GPCR and Y the relative residue number.
To select by the sequential residue numbering, use the option '-rn'.
In both options, multiple residues can be selected. Their IDs have to be separated by a whitespace and everything enclosed in quotation marks.
If both options are provided, only residues that fulfill both conditions will be printed. For example,

    python -m gpcrmining.gpcrdb -n adrb1_human -id "6.24 6.27 6.50" -rn "34 313 339"
    
only prints the following:

    Residue mapping for adrb1_human, using directory ./data-gpcrdb.
    TM6  313 R 6.24x24
    TM6  339 P 6.50x50

Available formats are 'plain' and 'drormd'. The specific DrorMD format has an option to define one or multiple segment IDs.
For example, 

    python -m gpcrmining.gpcrdb -n adrb1_human -id "6.24 6.27 6.50" -f drormd -s 'P0 P1'

prints the numbers in a format that can be directly copied into a DrorMD conditions file:

    Residue mapping for adrb1_human, using directory ./data-gpcrdb.
    'R6x24': 'segid P0 P1 and resid 313'
    'A6x27': 'segid P0 P1 and resid 316'
    'P6x50': 'segid P0 P1 and resid 339'

    
