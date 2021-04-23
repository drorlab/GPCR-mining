from .sequence import *

@click.command()
@click.option('-n', '--name', type=str, required=True)
@click.option('-d', '--directory', type=click.Path(exists=False), default='./data-gpcrdb')
@click.option('-id', '--gpcrdb-id', type=str, default='')
@click.option('-rn', '--res_num', type=str, default='')
@click.option('-f', '--fmt', type=str, default='plain')
@click.option('-s', '--segid', type=str, default='R')
def main(name, directory, gpcrdb_id, res_num, fmt, segid):
    gpcrdb_id = [i for i in gpcrdb_id.split(' ') if i] 
    res_num = [i for i in res_num.split(' ') if i] 
    print('Residue mapping for '+name+', using directory '+directory+'.')
    if not Path(directory).joinpath('gpcrdb-residues_'+name+'.csv').is_file():
        res_info = download_gpcrdb_residues(name, directory=directory, show=False)
    res_array = load_as_array(name, directory)
    if len(gpcrdb_id) > 0:
        res_array = select_by_gpcrdbnum(res_array, gpcrdb_id)
    if len(res_num) > 0:
        res_array = select_by_resnum(res_array, res_num)
    print_residues(res_array, fmt=fmt, segid=segid)


if __name__ == "__main__":
    main()

