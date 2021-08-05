"""
Commandline interface
"""
import click
import shutil
from yaml import safe_load
from vesta_colour_scheme.settings import DotVesta

@click.command('vesta-apply-colours')
@click.argument('vesta', type=click.Path(exists=True))
@click.argument('scheme', type=click.File('r'))
def main(vesta, scheme):
    """
    A apply a predefined colours to a VESTA file
    """

    obj = DotVesta(vesta)
    colours = safe_load(scheme)

    if 'tetra_mapping' in colours:
        obj.apply_colour_mapping(**colours)
    else:
        obj.apply_colour_mapping(colours)

    shutil.move(vesta, vesta + '.bak')
    click.echo(f'Backed up {vesta} to {vesta}.bak')
    obj.write(vesta)
    click.echo(f'{vesta} updated with the colour scheme')

if __name__ == '__main__':

    main()