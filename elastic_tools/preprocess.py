import json
from pathlib import Path
from typing import List

from pymatgen.analysis.elasticity.strain import DeformedStructureSet, Strain
from pymatgen.io.vasp import Poscar


def make_deformed_structures(
    inputs_dir: str,
    use_symmetry: bool = True,
    norm_strains: List[float] = None,
    shear_strains: List[float] = None,
) -> None:
    """Make deformed structures as POSCAR format

    Args:
        inputs_dir (str): path to inputs directory. New POSCARs will be saved there.
        use_symmetry (bool, optional): Whether to use symmetry. Defaults to True.
        norm_strains (List[float], optional): list of norm strains to apply.
            Defaults to None.
        shear_strains (List[float], optional): list of shear strains to apply.
            Defaults to None.
    """
    poscar_filename = "/".join([inputs_dir, "POSCAR"])
    poscar = Poscar.from_file(poscar_filename)
    if norm_strains is None:
        norm_strains = [-1e-5, 1e-5]
    if shear_strains is None:
        shear_strains = [0.5 * strain for strain in norm_strains]
    deformed_structures = DeformedStructureSet(
        poscar.structure,
        symmetry=use_symmetry,
        norm_strains=norm_strains,
        shear_strains=shear_strains,
    )

    for i, structure in enumerate(deformed_structures):
        deformed_dir_path = Path(inputs_dir) / f"deform-{str(i+1).zfill(3)}"
        if not deformed_dir_path.exists():
            deformed_dir_path.mkdir(parents=True)

        new_poscar_path = deformed_dir_path / "POSCAR"
        new_poscar = Poscar(structure)
        new_poscar.write_file(new_poscar_path, significant_figures=17)

        strain = Strain.from_deformation(deformed_structures.deformations[i])
        strain_json_path = deformed_dir_path / "strain.json"
        with strain_json_path.open("w") as f:
            json.dump(strain.as_dict(), f, indent=4)
