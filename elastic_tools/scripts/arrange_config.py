import json
from pathlib import Path

import click

from elastic_tools.config import Config


@click.command()
@click.option(
    "--mode", required=True, help="The mode of calculation. preprocess or postprocess."
)
@click.option("--calc_dir", required=True, help="The path to calculation directory.")
@click.option("--inputs_dir", required=True, help="The path to inputs directory.")
@click.option(
    "--by_vasp/--no-by_vasp",
    default=True,
    show_default=True,
    help="Whether VASP is used or not.",
)
@click.option(
    "--is_paramagnetic/--no-is_paramagnetic",
    default=False,
    show_default=True,
    help="Whether the system is paramagnetic or not.",
)
@click.option(
    "--use_symmetry/--no-use_symmetry",
    default=True,
    show_default=True,
    help="Whether symmetry is used or not.",
)
@click.option(
    "--norm_strains",
    type=str,
    default=None,
    show_default=True,
    help="The norm strains to apply. Use comma to seperate e.g) 0.1,-0.1",
)
@click.option(
    "--shear_strains",
    type=str,
    default=None,
    show_default=True,
    help="The shear strains to apply. Use comma to seperate e.g) 0.1,-0.1",
)
def main(
    mode,
    calc_dir,
    inputs_dir,
    by_vasp,
    is_paramagnetic,
    use_symmetry,
    norm_strains,
    shear_strains,
) -> None:
    """User interface to arrange config.json for elastic constants calculation"""
    # Convert relative path to absolute path
    calc_dir = str(Path(calc_dir).resolve())
    inputs_dir = str(Path(inputs_dir).resolve())

    config = Config(
        mode=mode,
        calc_dir=calc_dir,
        inputs_dir=inputs_dir,
        by_vasp=by_vasp,
        is_paramagnetic=is_paramagnetic,
        use_symmetry=use_symmetry,
        norm_strains=norm_strains,
        shear_strains=shear_strains,
    )

    json_path = Path(calc_dir) / f"{mode}.json"
    with json_path.open("w") as f:
        json.dump(config.to_dict(), f, indent=4)  # type: ignore


if __name__ == "__main__":
    main()
