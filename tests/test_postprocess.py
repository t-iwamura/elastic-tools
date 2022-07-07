import numpy as np

from elastic_tools.postprocess import calc_elastic_constants


def test_elastic_constants(al_dir_path):
    stiffness = calc_elastic_constants(str(al_dir_path))
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
    np.testing.assert_allclose(stiffness, expected_stiffness, rtol=0.3)
