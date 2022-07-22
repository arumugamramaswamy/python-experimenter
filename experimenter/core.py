from experimenter.exceptions import MainNotDefinedException
from experimenter.config_node import ConfigNode
from pathlib import Path
from .git_utils import GitRepo

import typing as T
import click
import glob
import os
import shutil
import logging

EXPERIMENT_DIR_NAME = "experimenter-results"

logger = logging.getLogger(__name__)

class Experiment:
    def __init__(self, allow_dirty: bool = False) -> None:
        self.allow_dirty = allow_dirty
        self._main: T.Optional[T.Callable[[T.Any, str], None]] = None

        @click.group("ex")
        def command_group():
            pass

        self.group = command_group

    @staticmethod
    def load_cfg(cfg_node_path) -> ConfigNode:
        return ConfigNode.yaml_load(cfg_node_path)
        
    def main(self, func: T.Optional[T.Callable[[T.Any, str], None]]):
        self._main = func

    def _get_experiment_dir_name(self, base_dir, name):
        experiment_base_path = os.path.join(base_dir, EXPERIMENT_DIR_NAME)
        max_run_id = 0
        for path in glob.glob(os.path.join(experiment_base_path, f"{glob.escape(name)}_[0-9]*")):
            file_name = path.split(os.sep)[-1]
            ext = file_name.split("_")[-1]
            if name == "_".join(file_name.split("_")[:-1]) and ext.isdigit() and int(ext) > max_run_id:
                max_run_id = int(ext)
        experiment_path = os.path.join(experiment_base_path, f"{name}_{max_run_id + 1}")
        Path(experiment_path).mkdir(parents=True, exist_ok=True)
        return experiment_path

    def run(self):
        @self.group.command(
            name = "run", help="Run Experiment"
        )
        @click.argument("cfg_node_path", type=click.Path(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True
        ))
        @click.argument("name")
        def run_exp(cfg_node_path, name):
            if self._main is None:
                raise MainNotDefinedException
            repo = GitRepo()

            dirty = repo.is_dirty()
            commit_hash = repo.get_current_commit()
            repo_base_dir = repo.get_base_dir()

            if dirty:
                logger.warn("Repo state is dirty")
                if not self.allow_dirty:
                    return

            experiment_config = ConfigNode()

            cfg_node = self.load_cfg(cfg_node_path)
            experiment_config.cfg = cfg_node

            experiment_config.repo = ConfigNode()
            experiment_config.repo.base_dir = repo_base_dir
            experiment_config.repo.dirty = dirty
            experiment_config.repo.commit_hash = commit_hash

            experiment_dir = self._get_experiment_dir_name(repo_base_dir, name)

            experiment_config.yaml_dump(os.path.join(experiment_dir, "cfg-w-meta.yaml"))
            shutil.copy(cfg_node_path, os.path.join(experiment_dir, "cfg.yaml"))

            self._main(cfg_node, experiment_dir)

        self.group()
