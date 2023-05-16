import json
from pathlib import Path
from typing import List, Tuple

from pymatgen.analysis.elasticity.strain import Strain
from pymatgen.analysis.elasticity.stress import Stress
from pymatgen.io.vasp import Vasprun


def parse_stress_and_strain(
    deform_dir_path: Path, by_vasp: bool = True
) -> Tuple[Stress, Strain]:
    """Parse stress and strain in deform-??? directory

    Args:
        deform_dir_path (Path): path to deform-??? directory.
        by_vasp (bool): Whether the result is calculated by VASP or not.

    Returns:
        Tuple[Stress, Strain]: tuple of Stress object and Strain object.
    """
    # Parse stress in deform-???/sp
    sp_dir_path = deform_dir_path / "sp"
    if by_vasp:
        vasprun_xml_path = sp_dir_path / "vasprun.xml"
        vasprun = Vasprun(str(vasprun_xml_path), parse_potcar_file=False)
        stress = Stress(vasprun.ionic_steps[-1]["stress"])
    else:
        predict_json_path = deform_dir_path / "predict.json"
        with predict_json_path.open("r") as f:
            predict_dict = json.load(f)
        stress = Stress(predict_dict["stress"])

    strain_json_path = sp_dir_path / "strain.json"
    with strain_json_path.open("r") as f:
        strain_dict = json.load(f)
    strain = Strain.from_dict(strain_dict)

    return stress, strain


def read_calc_results(
    calc_dir: str, by_vasp: bool = True
) -> Tuple[List[Stress], List[Strain], Stress]:
    """Read stress calculation results in calculation directory

    Args:
        calc_dir (str): Path to calculation directory.
        by_vasp (bool): Whether the result is calculated by VASP or not.

    Returns:
        Tuple[List[Stress], List[Strain], Stress]: The calculation results
    """
    # Parse stress and strain data in deform_set/deform-???
    deform_set_dir_path = Path(calc_dir) / "deform_set"
    deform_dir_list = [
        dir_path for dir_path in deform_set_dir_path.glob("deform-[0-9][0-9][0-9]")
    ]
    stress_list, strain_list = zip(
        *[
            parse_stress_and_strain(dir_path, by_vasp=by_vasp)
            for dir_path in deform_dir_list
        ]
    )

    # Parse stress of equilibrium structure
    eq_structure_dir_path = Path(calc_dir) / "eq_structure" / "sp"
    if by_vasp:
        eq_vasprun_xml_path = eq_structure_dir_path / "vasprun.xml"
        eq_vasprun = Vasprun(str(eq_vasprun_xml_path), parse_potcar_file=False)
        eq_stress = Stress(eq_vasprun.ionic_steps[-1]["stress"])
    else:
        predict_json_path = eq_structure_dir_path / "predict.json"
        with predict_json_path.open("r") as f:
            predict_dict = json.load(f)
        eq_stress = Stress(predict_dict["stress"])

    return stress_list, strain_list, eq_stress
