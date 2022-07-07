import logging

import click

from elastic_tools.config import load_config
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
        logging.info(f"     inputs dir: {config.inputs_dir}")
        logging.info(" Make deformed structures")
        make_deformed_structures(config.inputs_dir, use_symmetry=config.use_symmetry)

    if config.mode == "postprocess":
        pass
