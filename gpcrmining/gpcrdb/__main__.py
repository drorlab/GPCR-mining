from .sequence import *

@click.command()
@click.option('-n', '--name', type=str, required=True)
@click.option('-d', '--directory', type=click.Path(exists=False))
@click.option('--verbose/--no-verbose', default=False)
def main(name, directory='.', verbose=False):
    print('writing file to '+directory)
    res_info = download_gpcrmd_residues(name, directory=directory, show=verbose)


if __name__ == "__main__":
    main()

