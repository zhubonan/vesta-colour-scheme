"""
Test the functionality of the settings
"""
import shutil
import pytest
from pathlib import Path

from vesta_colour_scheme.settings import DotVesta, apply_colour_scheme, hex2rgb

@pytest.fixture
def datafolder():
    """Return the path of the test data folder"""
    return Path(__file__).parent / 'testdata'


@pytest.fixture
def cdte(datafolder):
    """Return the cdte.vesta file"""
    return DotVesta(str(datafolder / 'cdte.vesta'))

def test_settings(cdte, tmp_path):
    """Test the settings object"""

    assert cdte['TITLE'][0] == ''
    assert cdte['TITLE'][1] == ['Cd1 Te1', '']
    assert cdte['COMPS'][0] == '1'
    assert cdte['COMPS'][1] == []

    # Test round-trip read/write
    cdte.write(tmp_path / 'new.vesta')
    new = DotVesta(tmp_path / 'new.vesta')
    assert new.entries == cdte.entries

def test_apply_colour(cdte, tmp_path):
    """Test apply a colour scheme"""
    cdte.apply_colour_mapping({'Cd': {'rgb': '85D2D0', 'alpha': 50}, 'Te': {'rgb': '887BB0'}})
    assert cdte['ATOMT'][1][0] == '  1         Cd  1.5200 133 210 208 133 210 208  50'
    assert cdte['SITET'][1][0] == '  1         Cd0  1.5200 133 210 208 133 210 208  50  0'
    assert cdte['ATOMT'][1][1] == '  2         Te  1.3700 136 123 176 136 123 176 204'
    assert cdte['SITET'][1][1] == '  2         Te1  1.3700 136 123 176 136 123 176 204  0'

def test_hex2rgb():
    """Test converting HEX to RGB integers"""
    assert hex2rgb('85D2D0') == (133, 210, 208)

def test_apply_scheme(datafolder, tmp_path):
    """Test apply the colour scheme read from a file"""
    shutil.copy2(datafolder / 'cdte.vesta', tmp_path / 'cdte.vesta')
    apply_colour_scheme(tmp_path / 'cdte.vesta', datafolder / 'colours.yaml')
    dot = DotVesta(tmp_path / 'cdte.vesta')
    assert dot['ATOMT'][1][1] == '  2         Te  1.3700 136 123 176 136 123 176 204'