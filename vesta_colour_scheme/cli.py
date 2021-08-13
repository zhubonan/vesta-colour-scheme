"""
Commandline interface
"""
import click
import shutil
from yaml import safe_load
from vesta_colour_scheme.dotvesta import DotVesta

@click.command('vesta-apply-colours')
@click.option('--scheme', type=click.File('r'), default='colours.yaml')
@click.option('--backup/--no-backup', default=False) 
@click.option('--verbose', is_flag=True, default=False) 
@click.argument('vesta_file', type=click.Path(exists=True), nargs=-1)
def main(vesta_file, scheme, backup, verbose):
    """
    Apply a predefined colour scheme to a VESTA file
    """

    colours = safe_load(scheme)

    # Iterate through all files
    for file_name in vesta_file:
        obj = DotVesta(file_name)
        if 'tetra_mapping' in colours:
            obj.apply_colour_mapping(**colours)
        else:
            obj.apply_colour_mapping(colours)

        if backup:
            shutil.move(file_name, file_name + '.bak')
        if verbose:
            click.echo(f'Backed up {file_name} to {file_name}.bak')
        obj.write(file_name)
        if verbose:
            click.echo(f'{file_name} updated with the colour scheme')

if __name__ == '__main__':

    main()