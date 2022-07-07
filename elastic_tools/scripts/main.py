import click

from elastic_tools.config import load_config
from elastic_tools.preprocess import make_deformed_structures


@click.command()
@click.argument("config_file", nargs=1)
def main(config_file):
    """Tools for elastic constants calculation"""
    config = load_config(config_file)

    if config.mode == "preprocess":
        make_deformed_structures(config.inputs_dir)

    if config.mode == "postprocess":
        pass
