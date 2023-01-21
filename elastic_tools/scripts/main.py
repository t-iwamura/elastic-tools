import logging

import click
import numpy as np
from pymatgen.analysis.elasticity.elastic import ElasticTensor

from elastic_tools.config import load_config
from elastic_tools.postprocess import read_calc_results
from elastic_tools.preprocess import arrange_deform_set_dir


@click.command()
@click.argument("config_file", nargs=1)
def main(config_file):
    """Tools for elastic constants calculation"""
    logging.basicConfig(level=logging.DEBUG)
    logging.info(" Load config file")
    config = load_config(config_file)

    if config.mode == "preprocess":
        logging.info(" Start preprocess for elastic constants calculation")
        logging.info(f"     calculation dir: {config.calc_dir}")
        logging.info(" Make deformed structures")
        norm_strains, shear_strains = None, None
        if config.norm_strains is not None:
            norm_strains = list(config.norm_strains)
        if config.shear_strains is not None:
            shear_strains = list(config.shear_strains)
        arrange_deform_set_dir(
            config.calc_dir,
            config.inputs_dir,
            use_symmetry=config.use_symmetry,
            norm_strains=norm_strains,
            shear_strains=shear_strains,
        )

    if config.mode == "postprocess":
        stress_list, strain_list, eq_stress = read_calc_results(config.calc_dir)
        et = ElasticTensor.from_independent_strains(
            strains=strain_list,
            stresses=stress_list,
            eq_stress=eq_stress,
            vasp=True,
            tol=1e-4,
        )
        stiffness_filename = "/".join([config.calc_dir, "stiffness.txt"])
        np.savetxt(stiffness_filename, et.voigt, fmt="%.4e")
