# vesta-colour-scheme

Manipulating VESTA save files to apply user-defined colours.

This package provides an python inteface for reading/writing VESTA save files. It is very basic but serves the goal of changing colours well.
Picking a good colour scheme can quickly become non-trivial for systems with three or more elements.
The colour scheme should be sufficient for distinguishing different species, while not having too much "contrast" to strain the eye.

VESTA stores the default colours in the `elements.ini` inside the installation folder.
However, changing the `elements.ini` does not affect existing `.vesta` files that has been saved.
While colours of each species can be picked manually using GUI, the process of applying this to many `.vesta` files quickly becomes time-consuming and boring (especially for last-minute changes).

This package provides a command-line tool for applying a colour scheme, defined in a `*.yaml` file, to existing `.vesta` files.
This allows different colour scheme can be trialed and applied to a range of `.vesta` files easily.


## Installation

```
pip install git+https://github.com/zhubonan/vesta-colour-scheme.git#egg=vesta-colour-scheme
```


## Usage

Commandline interface:

```
Usage: vesta-colour-scheme [OPTIONS] VESTA SCHEME

  A apply a predefined colours to a VESTA file

Options:
  --help  Show this message and exit.
```


Example colour scheme file (`colours.yaml`):

```
Te:
        rgb: 887BB0
Cd:
        rgb: 85D2D0

# Integer RGB values also works
#Cd:
#        rgb: [100, 200, 0]
```

Once the `.vesta` file is updated, it must be re-opened with VESTA to see the changes.
An example `colours.yaml` can be found inside the `examples` folder.