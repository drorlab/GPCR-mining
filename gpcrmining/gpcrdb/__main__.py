from .sequence import *


def _split_argument(arg):
    return [i for i in arg.split(' ') if i] 


@click.command()
@click.option('-n', '--name', type=str, required=True)
@click.option('-d', '--directory', type=click.Path(exists=False), default='./data-gpcrdb')
@click.option('-id', '--gpcrdb-id', type=str, default='')
@click.option('-rn', '--res_num', type=str, default='')
@click.option('-p', '--part', type=str, default='')
@click.option('-f', '--fmt', type=str, default='plain')
@click.option('-s', '--segid', type=str, default='R')
@click.option('--write/--no-write', type=bool, default=True)
def main(name, directory, gpcrdb_id, res_num, part, fmt, segid, write):

    # Create lists from string arguments.
    gpcrdb_id = _split_argument(gpcrdb_id)
    res_num = _split_argument(res_num)
    part = _split_argument(part)
    name = _split_argument(name)

    # Loop over all receptor entries.
    for entry in name:
    
        # Obtain information for all residues in this entry.
        msg = 'Residue mapping for '+entry
        if write:
            msg += ', using directory '+directory+'.'
            if not Path(directory).joinpath('gpcrdb-residues_'+entry+'.csv').is_file():
                res_info = download_gpcrdb_residues(entry, directory=directory, show=False)
            res_info = load_as_array(entry, directory) if write else res_info
        else:
            msg += ', using no directory on disk.'
            res_info = download_gpcrdb_residues(entry, directory=None, show=False)
        
        # Select residues to print.        
        if len(gpcrdb_id) > 0:
            res_info = select_by_gpcrdbnum(res_info, gpcrdb_id)
        if len(res_num) > 0:
            res_info = select_by_resnum(res_info, res_num)
        if len(part) > 0:
            res_info = select_by_part(res_info, part)
            
        # Print the residues.
        print(msg)
        print_residues(res_info, fmt=fmt, segid=segid)


if __name__ == "__main__":
    main()

