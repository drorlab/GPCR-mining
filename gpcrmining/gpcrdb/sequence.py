import os
import click
import requests
import numpy as np
from pathlib import Path

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
    info = []
    for res in residue_html:
        res_part = res[2].split('>')[1]
        res_seqn = res[3].split(' # ')[1][1:]
        res_code = res[-3].split(' ')[-1]
        if len(res) == 12 and 'GPCRdb' in res[5]:
            res_dbid = res[5].split(' # ')[-1][1:]
        else:
            res_dbid = ''
        info.append([res_part, res_seqn, res_code, res_dbid])
    return info


def download_gpcrdb_residues(name, directory='.', show=False):
    """
    Downloads a sequence from GPCRdb and saves it as CSV file.
    
    Parameters
    ----------
        name : str
            Name of the GPCR to download (as in its GPCRdb URL). 
        directory : str
            Target directory.
            The directory is created if it does not exist.
        show : bool
            Print the sequence to the terminal.
    """  
    url = 'https://gpcrdb.org/protein/'+name+'/'
    req = requests.get(url, allow_redirects=True)
    txt = req.content.decode(req.encoding)
    residue_html = _extract_gpcrdb_residue_html(txt)
    residue_info = _extract_gpcrdb_residue_info(residue_html)
    # Write information to file
    Path(directory).mkdir(parents=True, exist_ok=True)
    out_filename = Path(directory).joinpath('gpcrdb-residues_'+name+'.csv')
    np.savetxt(out_filename, residue_info, delimiter=',', fmt='%s')
    if show:
        for res in residue_info:
            print('%6s %4s %1s %s'%(res[0],res[1],res[2],res[3]))
    return residue_info

