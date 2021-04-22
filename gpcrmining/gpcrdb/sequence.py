import os
import click
import requests
import numpy as np
from pathlib import Path

def _extract_gpcrmd_residue_html(txt):
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


def _extract_gpcrmd_residue_info(residue_html):
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


def download_gpcrmd_residues(name, directory='.', show=False):
    url = 'https://gpcrdb.org/protein/'+name+'/'
    req = requests.get(url, allow_redirects=True)
    txt = req.content.decode(req.encoding)
    residue_html = _extract_gpcrmd_residue_html(txt)
    residue_info = _extract_gpcrmd_residue_info(residue_html)
    # Write information to file
    Path(directory).mkdir(parents=True, exist_ok=True)
    out_filename = Path(directory).joinpath('gpcrdb-residues_'+name+'.csv')
    #out_filename = os.path.join(directory,'gpcrdb-residues_'+name+'.csv')
    np.savetxt(out_filename, residue_info, delimiter=',', fmt='%s')
    if show:
        for res in residue_info:
            print('%6s %4s %1s %s'%(res[0],res[1],res[2],res[3]))
    return residue_info

