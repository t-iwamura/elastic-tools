import json
from pathlib import Path
from typing import Tuple

from numpy.typing import NDArray
from pymatgen.analysis.elasticity.elastic import ElasticTensor
from pymatgen.analysis.elasticity.strain import Strain
from pymatgen.analysis.elasticity.stress import Stress
from pymatgen.io.vasp import Vasprun


def parse_stress_and_strain(deform_dir_path: Path) -> Tuple[Stress, Strain]:
    """Parse stress and strain in deform-??? directory

    Args:
        deform_dir_path (Path): path to deform-??? directory

    Returns:
        Tuple[Stress, Strain]: tuple of Stress object and Strain object
    """
    vasprun_xml_path = deform_dir_path / "vasprun.xml"
    vasprun = Vasprun(str(vasprun_xml_path))
    stress = Stress(vasprun.ionic_steps[-1]["stress"])

    strain_json_path = deform_dir_path / "strain.json"
    with strain_json_path.open("r") as f:
        strain_dict = json.load(f)
    strain = Strain.from_dict(strain_dict)

    return stress, strain


def calc_elastic_constants(inputs_dir: str) -> NDArray:
    """Calculate elastic constants from stress and strain data

    Args:
        inputs_dir (str): path to inputs directory where deform-??? directories exist

    Returns:
        NDArray: elastic stiffness tensor
    """
    inputs_dir_path = Path(inputs_dir)
    deform_dir_list = [
        dir_path for dir_path in inputs_dir_path.glob("deform-[0-9][0-9][0-9]")
    ]
    stress_list, strain_list = zip(
        *[parse_stress_and_strain(dir_path) for dir_path in deform_dir_list]
    )

    eq_vasprun_xml_path = inputs_dir_path / "vasp_outputs" / "vasprun.xml"
    eq_vasprun = Vasprun(str(eq_vasprun_xml_path))
    eq_stress = eq_vasprun.ionic_steps[-1]["stress"]

    et = ElasticTensor.from_independent_strains(
        strains=strain_list, stresses=stress_list, eq_stress=eq_stress, vasp=True
    )
    return et.voigt
