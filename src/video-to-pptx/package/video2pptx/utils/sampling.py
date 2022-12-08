import typing
from typing import Any

import numpy as np


def sample_linspace(
    data: typing.Sequence[Any], num_samples: int, num_desired_samples: int
) -> typing.List[Any]:
    """It samples a sequence of data samples as evenly spaced samples"""
    selected = np.linspace(0, num_samples - 1, num_desired_samples)
    selected = np.round(selected).astype(int)

    data_samples = [sample for idx, sample in enumerate(data) if idx in selected]

    return data_samples
