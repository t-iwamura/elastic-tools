from pathlib import Path

from pymatgen.analysis.elasticity.strain import DeformedStructureSet
from pymatgen.io.vasp import Poscar


def make_deformed_structures(inputs_dir: str, use_symmetry: bool = True) -> None:
    """Make deformed structures as POSCAR format

    Args:
        inputs_dir (str): path to inputs directory. New POSCARs will be saved there.
        use_symmetry (bool): Whether to use symmetry. Defaults to True.
    """
    poscar_filename = "/".join([inputs_dir, "POSCAR"])
    poscar = Poscar.from_file(poscar_filename)
    deformed_structures = DeformedStructureSet(poscar.structure, symmetry=use_symmetry)

    for i, structure in enumerate(deformed_structures):
        deformed_dir_path = Path(inputs_dir) / f"deform-{str(i+1).zfill(3)}"
        if not deformed_dir_path.exists():
            deformed_dir_path.mkdir(parents=True)

        new_poscar_path = deformed_dir_path / "POSCAR"
        new_poscar = Poscar(structure)
        new_poscar.write_file(new_poscar_path)
