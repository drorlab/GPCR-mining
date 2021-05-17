import os
import click
import requests
import numpy as np
from pathlib import Path


# Functions to obtain residue information from the GPCRdb


def download_gpcrdb_residues(name, directory=None, show=False, scrape=False):
    """
    Downloads a sequence with segment annotations and sequential+generic residue numbers from GPCRdb. 
    Optionally saves it as CSV file or prints it to the command line.
    
    Parameters
    ----------
        name : str
            Name of the GPCR to download (as in its GPCRdb URL). 
        directory : str
            Target directory.
            The directory is created if it does not exist.
        show : bool
            Print the sequence to the terminal.
            
    Returns
    -------
        residue_info : list
            A list in which each item contains the following strings:
            - part of the residue
            - sequential residue number
            - amino acid 1-letter code
            - GPCRdb residue ID
            
    """  
    # Fetch data from GPCRdb
    if scrape: 
        # scrape info from the website HTML (outdated, for test purposes only)
        residue_info = scrape_residue_info(name)
    else: 
        # retrieve info via the GPCRdb API
        residue_info = get_residue_info(name)
    # Write information to CSV file
    if directory is not None:
        Path(directory).mkdir(parents=True, exist_ok=True)
        out_filename = Path(directory).joinpath('gpcrdb-residues_'+name+'.csv')
        np.savetxt(out_filename, residue_info, delimiter=',', fmt='%s', 
                   header='Part, SeqID, Code, GPCRdbID')
    # Print information to screen
    if show:
        for res in residue_info:
            print('%6s %4s %1s %s'%(res[0],res[1],res[2],res[3]))
    return residue_info
    
    
def get_residue_info(name):
    """
    Gets residue info from the GPCRdb API
    
    Parameters
    ----------
        name : str
            Name of the GPCR to download (as in its GPCRdb URL). 
            
    Returns
    -------
        residue_info : list
            A list in which each item contains the following strings:
            - part of the residue
            - sequential residue number
            - amino acid 1-letter code
            - GPCRdb residue ID
    """
    # Fetch the protein 
    url = 'https://gpcrdb.org/services/protein/'+name
    response = requests.get(url)
    protein_data = response.json()
    # Determine the numbering scheme to use
    num_scheme = protein_data['residue_numbering_scheme']
    # Fetch the residue information
    url = 'https://gpcrdb.org/services/residues/extended/'+name
    response = requests.get(url)
    residue_data = response.json()
    # Extract info in array format
    residue_info = []
    for res in residue_data:
        res_part = res['protein_segment']
        res_seqn = res['sequence_number']
        res_code = res['amino_acid']
        res_dbid = ''
        for num in res['alternative_generic_numbers']:
            if num['scheme'] == num_scheme:
                res_dbid = num['label']
        residue_info.append([res_part, res_seqn, res_code, res_dbid])
    return residue_info


def scrape_residue_info(name):
    """
    Scrapes residue info from the GPCRdb website html
    
    Parameters
    ----------
        name : str
            Name of the GPCR to download (as in its GPCRdb URL). 
            
    Returns
    -------
        residue_info : list
            A list in which each item contains the following strings:
            - part of the residue
            - sequential residue number
            - amino acid 1-letter code
            - GPCRdb residue ID
    """
    url = 'https://gpcrdb.org/protein/'+name+'/'
    req = requests.get(url, allow_redirects=True)
    txt = req.content.decode(req.encoding)
    residue_html = _extract_gpcrdb_residue_html(txt)
    residue_info = _extract_gpcrdb_residue_info(residue_html)
    return residue_info
    
    
def _extract_gpcrdb_residue_html(txt):
    """
    Extracts the relevant lines for all residues from a GPCRdb html entry.
    
    Parameters
    ----------
        txt : str
            Content (html) of the website with the GPCRdb entry.

    Returns
    -------
        residue_html : list
            A list in which each item contains the html lines for one residue.
            
    """  
    res_start_line = '                        <td class="seqv seqv-sequence">'
    res_end_line = '                        </td>'
    spl = txt.split('\n')
    residue_html = []
    for lnum, line in enumerate(spl):
        if line == res_start_line:
            residue_lines = spl[lnum:lnum+12]
            # Use fewer lines if the residue is shorter
            # (i.e. has no GPCRdb number)
            if residue_lines[-4] == res_end_line:
                residue_lines = residue_lines[:-3]
            residue_html.append(residue_lines)
    return residue_html


def _extract_gpcrdb_residue_info(residue_html):
    """
    Extracts the relevant info from GPCRdb html entries of residues.
    
    Parameters
    ----------
        residue_html : list
            A list in which each item contains the html lines for one residue.

    Returns
    -------
        residue_info : list
            A list in which each item contains the following strings:
            - part of the residue
            - sequential residue number
            - amino acid 1-letter code
            - GPCRdb residue ID
            
    """
    residue_info = []
    for res in residue_html:
        res_part = res[2].split('>')[1]
        res_seqn = res[3].split(' # ')[1][1:]
        res_code = res[-3].split(' ')[-1]
        if len(res) == 12 and 'GPCRdb' in res[5]:
            res_dbid = res[5].split(' # ')[-1][1:]
        else:
            res_dbid = ''
        residue_info.append([res_part, res_seqn, res_code, res_dbid])
    return residue_info

    

# Functions to load a receptor data file


def load_as_array(name, directory):
    filename = Path(directory).joinpath('gpcrdb-residues_'+name+'.csv')
    return np.loadtxt(filename ,dtype=str, delimiter=',', skiprows=1)


def load_as_dataframe(name, directory):
    filename = Path(directory).joinpath('gpcrdb-residues_'+name+'.csv')
    df = pd.read_csv(filename)
    for i in range(len(df.columns)):
        df.columns.values[i] = df.columns.values[i].split(' ')[-1]
    return df
    
    
# Functions to print and select residues
    

def print_residues(ar, fmt='plain', segid='R'):    
    for res in ar:      
        # Read out residue data and build labels
        resnum = res[1]
        if res[3] == '':
            reslabel = res[2]+res[1]
        else:
            reslabel = res[2]+res[3]            
        # Print if a valid format is given
        if fmt=='plain':
            print('%6s %4s %1s %s'%(res[0],res[1],res[2],res[3]))
        elif fmt=='drormd':
            drorlabel=reslabel.split('x')[0].replace('.','x')
            print("    '%s': 'segid %s and resid %s',"%(drorlabel, segid, resnum))           
    return
    
    
def select_by_gpcrdbnum(res_array, gpcrdb_num):
    out_list = []
    # Go through all residues
    for res in res_array:
        selected = False
        # Read out residue data and build labels
        resnum = res[1]
        if res[3] == '':
            reslabel = res[1]
            if reslabel in gpcrdb_num:
                selected = True
        else:
            reslabel = res[3]
            reslabel_bw = res[3].split('x')[0]
            reslabel_db = res[3].split('.')[0]+'x'+res[3].split('x')[1]
            if reslabel in gpcrdb_num:
                selected = True
            if reslabel_bw in gpcrdb_num:
                selected = True
            if reslabel_db in gpcrdb_num:
                selected = True
        # Add residue info if it is in the list
        if selected:
            out_list.append(res)
    return out_list


def select_by_resnum(res_array, res_num):    
    out_list = []   
    # Go through all residues
    for res in res_array:           
        # Add residue info if it is in the list
        if res[1] in res_num:
            out_list.append(res)
    return out_list


def select_by_part(res_array, parts):
    out_list = []
    # Go through all residues
    for res in res_array:
        # Add residue info if it is in the list
        if res[0] in parts:
            out_list.append(res)
    return out_list

    


