# GPCR-mining
Functions to scrape GPCR data from the web.

## Installation

You can install the python package via pip

    git clone https://github.com/drorlab/GPCR-mining
    cd GPCR-mining
    pip install -e .

To include the functions in your Python workflow, ipmport the library via

    import gpcrmining.gpcrdb
    
See below for an explanation on how to run the main script from the command line.

## GPCRdb sequence numbering

The [__GPCRdb__](https://gpcrdb.org) provides a comprehensive overview for the sequence of a GPCR, including definitions of transmembrane helices and generic residue numbering.
Looking up a large number of residues or including the conversion for a specific receptor into an automated workflow can become tedious. Here we provide code to download and display this data.

### Obtain the entire sequence

To obtain such a sequence and to save it in a more easily usable CSV file, run

    python -m gpcrmining.gpcrdb -n GPCR_NAME -d DIR

with "GPCR_NAME" being the name of the GPCR as used in the corresponding GPCRmd URL. "DIR" is the directory where the data should be saved (default: data-gpcrmd), which is created if it does not exist. For example,

    python -m gpcrmining.gpcrdb -n adrb1_human -d my-data-from-gpcrmd

writes the file _gpcrdb-residues_adrb1_human.csv_ into the directory _my-data-from-gpcrmd_.

### Select and print residues

To select residues by their sequential number, use the option _-rn_. To select multiple residues, their IDs have to be separated by a whitespace and everything enclosed in quotation marks.

    python -m gpcrmining.gpcrdb -n adrb1_human -rn "230 231 232 233 313 339" 
    
To select residues by a generic residue numbering scheme, use the option _-id_.
GPCRdb uses two similar [numbering systems](https://docs.gpcrdb.org/generic_numbering.html) (one sequence-based, following Ballesteros-Weistein, Wooten,... and one corrected for helix bulges).
By default, the code will return the combined format. 
For input, both formats can be used (BW etc. with a dot as separator and the GPCRdb format with x) as well as the combined one. Numbering schemes can be mixed, e.g.,

    python -m gpcrmining.gpcrdb -n adrb1_human -id "5.45 5x461 6.24 6.27 6.50x50"

To select defined parts of the receptor, use the option _-p_.

    python -m gpcrmining.gpcrdb -n adrb1_human -p "N-term TM7 ICL2"

If several selection flags are provided, only residues that fulfill all conditions will be printed. For example,

    python -m gpcrmining.gpcrdb -n adrb1_human -id "5.45 5x461 6.24 6.27 6.50x50" -rn "230 231 232 233 313 339"    
    
prints the following:

    Residue mapping for adrb1_human, using directory ./data-gpcrdb.
       TM5  231 V 5.45x46
       TM5  232 S 5.46x461
       TM6  313 R 6.24x24
       TM6  339 P 6.50x50

To obtain analogous residues across receptors, use a multiple-entry string, just as for the residues:

    python -m gpcrmining.gpcrdb -n "adrb1_human adrb2_human" -id "5.45 5x461 6.24 6.27 6.50x50"


### Output formats

Available output formats are 'plain' and 'drormd', with 'plain' (as above) being the default. 

If you would like to have another format added, you have two options:
- open an issue with a description of what you have in mind or
- fork the repo, implement your favorite format as an additional option, and open a pull request. 

The specific DrorMD format has an option to define one or multiple segment IDs.
For example, 

    python -m gpcrmining.gpcrdb -n adrb1_human -id "6.24 6.27 6.50" -f drormd -s 'P0 P1'

prints the numbers in a format that can be directly copied into a DrorMD conditions file:

    Residue mapping for adrb1_human, using directory ./data-gpcrdb.
    'R6.24x24': 'segid P0 P1 and resid 313'
    'A6.27x27': 'segid P0 P1 and resid 316'
    'P6.50x50': 'segid P0 P1 and resid 339'

    
