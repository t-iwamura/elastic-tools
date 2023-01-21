import logging
from pathlib import Path

import click
import numpy as np

from elastic_tools.config import load_config
from elastic_tools.postprocess import calc_elastic_constants
from elastic_tools.preprocess import make_deformed_structures


@click.command()
@click.argument("config_file", nargs=1)
def main(config_file):
    """Tools for elastic constants calculation"""
    logging.basicConfig(level=logging.DEBUG)
    logging.info(" Load config file")
    config = load_config(config_file)

    if config.mode == "preprocess":
        logging.info(" Start preprocess for elastic constants calculation")
        logging.info(f"     inputs dir: {config.calc_dir}")
        logging.info(" Make deformed structures")
        norm_strains, shear_strains = None, None
        if config.norm_strains is not None:
            norm_strains = list(config.norm_strains)
        if config.shear_strains is not None:
            shear_strains = list(config.shear_strains)
        make_deformed_structures(
            config.calc_dir,
            use_symmetry=config.use_symmetry,
            norm_strains=norm_strains,
            shear_strains=shear_strains,
        )

    if config.mode == "postprocess":
        stiffness = calc_elastic_constants(config.calc_dir)
        stiffness_path = Path(config.outputs_dir) / "stiffness.txt"
        np.savetxt(str(stiffness_path), stiffness, fmt="%.4e")
