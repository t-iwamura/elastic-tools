# elastic-tools
Python package to support elastic constants calculation

## Overview

This package helps users perform elastic constants calculation. By using this package, you can generate necessary deformed structures from an relaxed structure and calculate elastic stiffness by parsing the calculation results about the generated structures.

## Installation

```shell
$ cd <elastic-tools root>
$ pip install .
```

## Usage

To perform calculations, you have to arrange an config file. You can use a Python program to generate it. To display help messages, run the Python script with `--help` option.

```shell
$ python <elastic-tools root>/elastic_tools/scripts/arrange_config.py --help
Usage: arrange_config.py [OPTIONS]

  User interface to arrange config.json for elastic constants calculation

Options:
  --mode TEXT                     The mode of calculation. preprocess or
                                  postprocess.  [required]
  --calc_dir TEXT                 The path to calculation directory.
                                  [required]
  --inputs_dir TEXT               The path to inputs directory.  [required]
  --by_vasp / --no-by_vasp        Whether VASP is used or not.  [default:
                                  by_vasp]
  --is_paramagnetic / --no-is_paramagnetic
                                  Whether the system is paramagnetic or not.
                                  [default: no-is_paramagnetic]
  --use_symmetry / --no-use_symmetry
                                  Whether symmetry is used or not.  [default:
                                  use_symmetry]
  --norm_strains TEXT             The norm strains to apply. Use comma to
                                  seperate e.g) 0.1,-0.1
  --shear_strains TEXT            The shear strains to apply. Use comma to
                                  seperate e.g) 0.1,-0.1
  --help                          Show this message and exit.
```

### Preprocess

In preprocess, deformed structures are generated from an relaxed structure. After preprocess, you have to relax the atomic positions in each deformed structure and perform single point calculations to obtain the stress.

1. Suppose that you want to calculate elastic constants of Al. Create an calculation directory in `elastic-tools/data/outputs/Al/001`.
2. Arrange an POSCAR file of Al and relax the structure until the stress for it is approximately zero. Put the relaxed POSCAR file in an directory, `elastic-tools/data/outputs/Al/001/eq_structure/relax`.
3.  Make an directory, `elastic-tools/data/inputs/Al/001`. Then, arrange `INCAR`, `KPOINTS` and `POTCAR` used to relax the deformed structure and put them in the directory.
4. Run an following command and arrange an config file.
```shell
$ cd elastic-tools/data/outputs/Al/001
$ python <elastic-tools root>/elastic_tools/scripts/arrange_config.py --mode preprocess --calc_dir . --inputs_dir <elastic-tools root>/data/inputs/Al/001
```
You'll see an generated config file in your calculation directory.
```shell
$ ls .
preprocess.json
```
5. Generate deformed structures by performing an following command.
```shell
# Run an following command in your calculation directory
$ elastic-tools preprocess.json

# See generated directories
$ ls
deform_set/ eq_structure/ preprocess.json
$ ls deform_set
deform-001/ deform-003/ deform-005/ deform-007/
deform-002/ deform-004/ deform-006/ deform-008/
```

### Postprocess
1. Relax the atomic positions in the each deformed structure and run single point calculations to obtain stress after relaxation. Put the result of the single point calculation in an directory, `deform_set/deform-???/sp`.
2. Copy `preprocess.json` as `postprocess.json` and edit it.
```shell
$ cp preprocess.json postprocess.json
$ sed -i "s/preprocess/postprocess/" postprocess.json
```
3. Calculate elastic stiffness by parsing the calculation results.
```shell
$ elastic-tools postprocess.json
```
