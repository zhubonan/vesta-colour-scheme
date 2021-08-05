"""
Read, write and manipulate VESTA save files
"""
import re
import shutil
from typing import Tuple, List, Dict
from collections import OrderedDict
from pathlib import Path

from yaml import safe_load


class DotVesta:
    """
    Representation of a VESTA save file
    """
    def __init__(self, path: str):
        """
        Instantiate from an existing .vesta file
        """
        if isinstance(path, (str, Path)):
            self._content = Path(path).read_text().split('\n')
        elif hasattr(path, 'readlines'):
            self._content = path.readlines()
        else:
            raise ValueError(
                '<path> should a path-like object or a file object.')

        self.entries = read_content(self._content[2:])

    def __getitem__(self, key):
        return self.entries[key]

    def __setitem__(self, key, value):
        self.entries[key] = value

    def write(self, outfile: str) -> None:
        """
        Write the output file

        Args:
            outfile (str): Name of the output file.
        """
        with open(outfile, 'w') as fhandle:
            fhandle.write('#VESTA_FORMAT_VERSION 3.5.0\n\n')
            for name, item in self.entries.items():
                fhandle.write(name + ' ' + item[0] + '\n')  # Write the title line
                for line in item[1]:
                    fhandle.write(line + '\n')

    def apply_colour_mapping(self, mapping: dict, tetra_mapping=None) -> None:
        """
        Apply a userdefined colour mapping for each atoms

        Args:
            mapping (dict): A dictionary of the mappings with the RGB in the 'rgb' key and alpha under the 'alpha' key (for tetrahedron) for each specie
            tetra_mapping (dict): A dictionary of the mappings for the tetrahedron with the RGB in the 'rgb' key.

        """
        # More sure the values are in RGB numerical tuple
        for _mapping in [mapping, tetra_mapping]:
            if not _mapping:
                continue
            for key in _mapping:
                value = _mapping[key]['rgb']
                if isinstance(value, str):
                    _mapping[key]['rgb'] = hex2rgb(value)

        lines = self.entries['ATOMT'][1]
        self.entries['ATOMT'][1] = update_colour_lines(lines, mapping,
                                                       tetra_mapping)

        lines = self.entries['SITET'][1]
        self.entries['SITET'][1] = update_colour_lines(lines,
                                                       mapping,
                                                       tetra_mapping,
                                                       is_sitet=True)


def read_content(content: list) -> Dict[str, Tuple[str, List[str]]]:
    """
    Read each entry of the VESTA files

    Args:
        content (list): A list of lines read from a .vesta file

    Returns:
        A dictionary of name of values of each field.
    """
    current_name = None
    current_lines = []
    entries = OrderedDict()
    for line in content:
        if line.endswith('\n'):
            line = line[:-1]
        if not line:
            current_lines.append('')
            continue
        if line[0].isupper() and line[1].isupper():
            if current_name:
                entries[current_name] = [tagline, current_lines]
                current_lines = []

            # Get the new tag and tag line part
            tag = line.split()[0]
            current_name = tag
            tagline = line[len(tag) + 1:]
            continue

        current_lines.append(line)
    # Remote the last empty line
    if not current_lines[-1]:
        current_lines.pop() 
    entries[current_name] = (tagline, current_lines)

    return entries


def update_colour_lines(lines, mapping, tetra_mapping=None, is_sitet=False) -> List[str]:
    """
    Update the colour mapping for dotvesta for the ATOMT and SITET
    """
    new_lines = []
    for line in lines:
        tokens = line.split()
        # Use re to match sites like Li1, Fe2 etc.
        orig_name = tokens[1]
        match = re.match(r'([A-Za-z]+)\d*', tokens[1])
        # If not matching, just skip the line. The last line of the section will never match
        if not match:
            new_lines.append(line)
            continue

        atom_name = match.group(1)
        if atom_name in mapping:
            radius = tokens[2]
            r, g, b = mapping[atom_name]['rgb']

            # Assign the tetragonal mapping
            if tetra_mapping is not None and atom_name in tetra_mapping:
                tr, tg, tb = tetra_mapping[atom_name]['rgb']
            else:
                tr, tg, tb = r, g, b

            # Alpha for the tetrahedral
            if is_sitet:
                alpha = mapping[atom_name].get('alpha', int(tokens[-2]))
                line = f'{int(tokens[0]):>3d}{orig_name:>12}{radius:>8}{r:>4d}{g:>4d}{b:>4d}{tr:>4d}{tg:>4d}{tb:>4d}{alpha:>4d}  0'
            else:
                alpha = mapping[atom_name].get('alpha', int(tokens[-1]))
                line = f'{int(tokens[0]):>3d}{orig_name:>11}{radius:>8}{r:>4d}{g:>4d}{b:>4d}{tr:>4d}{tg:>4d}{tb:>4d}{alpha:>4d}'
            new_lines.append(line)
        else:
            new_lines.append(line)
    return new_lines


def hex2rgb(hex_string: str) -> Tuple[int, int, int]:
    """Convert a hexstring to RGB tuple"""
    hex_string = hex_string.lstrip('#')
    return tuple(int(hex_string[i:i + 2], 16) for i in (0, 2, 4))


def apply_colour_scheme(file: str, scheme: str) -> None:
    """
    Shortcut function for applying a colour scheme
    """

    obj = DotVesta(file)
    with open(scheme) as fhandle:
        colours = safe_load(fhandle)

    if 'tetra_mapping' in colours:
        obj.apply_colour_mapping(**colours)
    else:
        obj.apply_colour_mapping(colours)

    shutil.move(file, str(file) + '.bak')
    obj.write(file)