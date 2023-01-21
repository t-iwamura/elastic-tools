import json
from dataclasses import dataclass
from typing import Optional, Tuple

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Config:
    mode: str
    calc_dir: str
    inputs_dir: str
    use_symmetry: bool = True
    # strain values
    norm_strains: Optional[Tuple[float]] = None
    shear_strains: Optional[Tuple[float]] = None


def load_config(path: str) -> Config:
    """Load configs/*.json

    Args:
        path (str): path to configs/*.json

    Returns:
        Config: Elastic Constants calculation config dataclass
    """
    with open(path) as f:
        config_dict = json.load(f)
    return Config.from_dict(config_dict)  # type: ignore
