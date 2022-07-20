from pathlib import Path
from .git_utils import GitRepo

import typing as T
import click
import glob
import os

EXPERIMENT_DIR_NAME = "experimenter-results"

class Experiment:
    def __init__(self, name: str, allow_dirty: bool = False) -> None:
        self.name = name
        self.allow_dirty = allow_dirty
        self._main: T.Optional[T.Callable[[T.Any, str], None]] = None

    def main(self, func: T.Optional[T.Callable[[T.Any, str], None]]):
        self._main = func

    def _get_experiment_dir_name(self, base_dir):
        experiment_base_path = os.path.join(base_dir, EXPERIMENT_DIR_NAME)
        max_run_id = 0
        for path in glob.glob(os.path.join(experiment_base_path, f"{glob.escape(self.name)}_[0-9]*")):
            file_name = path.split(os.sep)[-1]
            ext = file_name.split("_")[-1]
            if self.name == "_".join(file_name.split("_")[:-1]) and ext.isdigit() and int(ext) > max_run_id:
                max_run_id = int(ext)
        experiment_path = os.path.join(experiment_base_path, f"{self.name}_{max_run_id + 1}")
        Path(experiment_path).mkdir(parents=True, exist_ok=True)
        return experiment_path

    def run(self):
        @click.command(
            name = "run"
        )
        @click.argument("cfg_node_path", type=click.File("r"))
        def run_exp(cfg_node_path):
            if self._main is None:
                raise ValueError
            repo = GitRepo()

            dirty = repo.is_dirty()
            commit_hash = repo.get_current_commit()
            repo_base_dir = repo.get_base_dir()

            if not self.allow_dirty and dirty:
                return

            cfg_node = None
            experiment_dir = self._get_experiment_dir_name(repo_base_dir)
            self._main(cfg_node, experiment_dir)

        run_exp()
