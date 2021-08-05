"""
Tests for the commandline interface
"""
from pathlib import Path
import shutil

import pytest
from vesta_colour_scheme.cli import main
from vesta_colour_scheme.dotvesta import DotVesta
from click.testing import CliRunner


@pytest.fixture
def datafolder():
    """Return the path of the test data folder"""
    return Path(__file__).parent / 'testdata'

def test_cli(datafolder):
    """Test teh commandline interface"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        shutil.copy2(datafolder / 'cdte.vesta', 'cdte.vesta')
        shutil.copy2(datafolder / 'colours.yaml', 'colours.yaml')
        runner.invoke(main, ['cdte.vesta', 'colours.yaml'])
        dot = DotVesta('cdte.vesta')
    
    assert dot['ATOMT'][1][1] == '  2         Te  1.3700 136 123 176 136 123 176 204'