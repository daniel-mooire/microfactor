"""Click CLI assembled from per-domain command modules."""

from microfactor.cli import (  # noqa: F401  (imports register commands on the group)
    compute_cmds,
    evaluate_cmds,
    preprocess_cmds,
    registry_cmds,
)
from microfactor.cli.root import cli

__all__ = ["cli"]
