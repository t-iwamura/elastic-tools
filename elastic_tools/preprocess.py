import json
import shutil
from copy import copy
from pathlib import Path
from typing import List

from pymatgen.analysis.elasticity.strain import DeformedStructureSet, Strain
from pymatgen.io.vasp import Poscar


def arrange_deform_set_dir(
    calc_dir: str,
    inputs_dir: str,
    is_paramagnetic: bool = False,
    use_symmetry: bool = True,
    norm_strains: List[float] = None,
    shear_strains: List[float] = None,
) -> None:
    """Arrange deform_set directory

    Args:
        calc_dir (str): Path to calculation directory.
        inputs_dir (str): Path to inputs directory.
        is_paramagnetic (str): Whether or not the structure is paramagnetic.
        use_symmetry (bool, optional): Whether to use symmetry. Defaults to True.
        norm_strains (List[float], optional): List of norm strains to apply.
            Defaults to None.
        shear_strains (List[float], optional): List of shear strains to apply.
            Defaults to None.
    """
    if norm_strains is None:
        norm_strains = [-1e-5, 1e-5]
    if shear_strains is None:
        shear_strains = [0.5 * strain for strain in norm_strains]

    # Generate Structure objects with deformation
    poscar_path = Path(calc_dir) / "eq_structure" / "relax" / "POSCAR"
    eq_structure = Poscar.from_file(str(poscar_path)).structure
    deformed_structures = DeformedStructureSet(
        eq_structure,
        symmetry=use_symmetry,
        norm_strains=norm_strains,
        shear_strains=shear_strains,
    )

    # Make a list of the files in inputs directory
    file_path_list = [path for path in Path(inputs_dir).glob("*")]

    deform_set_dir_path = Path(calc_dir) / "deform_set"
    for i, deformed_structure in enumerate(deformed_structures):
        deformed_dir_path = deform_set_dir_path / f"deform-{str(i+1).zfill(3)}"
        if not deformed_dir_path.exists():
            deformed_dir_path.mkdir(parents=True)

        strain = Strain.from_deformation(deformed_structures.deformations[i])
        strain_json_path = deformed_dir_path / "strain.json"
        with strain_json_path.open("w") as f:
            json.dump(strain.as_dict(), f, indent=4)

        # Copy files in inputs directory to deform directory
        for file_path in file_path_list:
            shutil.copyfile(file_path, deformed_dir_path / file_path.name)

        new_poscar = Poscar(deformed_structure)
        new_poscar_path = deformed_dir_path / "POSCAR"
        new_poscar.write_file(new_poscar_path, significant_figures=17)

        # Rewrite POSCAR to one with two species
        if is_paramagnetic:
            with new_poscar_path.open("r") as f:
                old_lines = f.readlines()

            element = old_lines[5].strip()
            n_atoms = int(old_lines[6].strip())
            n_atoms_half = n_atoms // 2

            new_lines = copy(old_lines)
            new_lines[5] = f"{element} {element}\n"
            new_lines[6] = f"{n_atoms_half} {n_atoms_half}\n"

            with new_poscar_path.open("w") as f:
                f.write("".join(new_lines))
