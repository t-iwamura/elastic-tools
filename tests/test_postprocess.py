import numpy as np
from pymatgen.analysis.elasticity.elastic import ElasticTensor

from elastic_tools.postprocess import read_calc_results


def test_elastic_constants(al_dir_path):
    stress_list, strain_list, eq_stress = read_calc_results(calc_dir=str(al_dir_path))
    et = ElasticTensor.from_independent_strains(
        strains=strain_list,
        stresses=stress_list,
        eq_stress=eq_stress,
        vasp=True,
        tol=1e-4,
    )
    expected_stiffness = np.array(
        [
            [104, 73, 73, 0, 0, 0],
            [73, 104, 73, 0, 0, 0],
            [73, 73, 104, 0, 0, 0],
            [0, 0, 0, 32, 0, 0],
            [0, 0, 0, 0, 32, 0],
            [0, 0, 0, 0, 0, 32],
        ]
    )
    np.testing.assert_allclose(et.voigt, expected_stiffness, rtol=0.3)
