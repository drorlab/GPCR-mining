import requests
import urllib
import io
import gzip
from pathlib import Path


def get_pdb_structure_info(pdbid):
    """
    Gets info about a PDB structure from the GPCRdb
    
    Parameters
    ----------
        pdbid : str
            PDB ID of the structure. Can be upper- or lowercase. 
            
    Returns
    -------
        structure_info : dict
            A dictionary with information about the PDB structure.
                
    """
    # Convert to uppercase
    pdbid = pdbid.upper()
    # Fetch the structure 
    url = 'https://gpcrdb.org/services/structure/'+pdbid
    response = requests.get(url)
    str_info = response.json()
    return str_info


def download_pdb_structure(pdbid, directory='.'):
    """
    Downloads a structure from the PDB.
    
    Parameters
    ----------
        pdbid : str
            PDB ID of the structure. Can be upper- or lowercase. 
        directory : str
            Directory in which to save the structure
            
    Returns
    -------
        pdbid : str
            PDB ID of the structure in lowercase.
                
    """    
    pdbid = pdbid.lower()

    Path(directory).mkdir(parents=True, exist_ok=True)
    out_filename = Path(directory).joinpath(pdbid+'.pdb')

    # Fetch the structure 
    url = 'https://files.rcsb.org/download/'+pdbid+'.pdb.gz'
    response = urllib.request.urlopen(url)
    compressed_file = io.BytesIO(response.read())
    decompressed_file = gzip.GzipFile(fileobj=compressed_file)

    with open(out_filename, 'wb') as outfile:
        outfile.write(decompressed_file.read())

    return pdbid

