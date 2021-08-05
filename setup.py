#!/usr/bin/env python

from setuptools import setup, find_packages

if __name__ == '__main__':
      setup(
        name='vesta-colour-scheme',
        author='Bonan Zhu',
        author_email="zhubonan@outlook.com",
        description='A simple tool to alter the colour scheme of VESTA',
        license='MIT License',
        version='0.1.0',
        install_requires=['PyYaml', 'click'],
        packages=find_packages(),
        entry_points={'console_scripts': ['vesta-colour-scheme=vesta_colour_scheme.cli:main']})
