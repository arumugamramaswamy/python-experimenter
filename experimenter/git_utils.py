from git.repo.base import Repo
from git.exc import InvalidGitRepositoryError
from pathlib import Path

import logging
import typing as T

logger = logging.getLogger(__name__)

class GitRepo:
    def __init__(self) -> None:
        try:
            self._repo = Repo()
        except InvalidGitRepositoryError:
            logger.warn("Could not find repo")
            self._repo = None

    def is_dirty(self) -> bool:
        """Check if current repo is dirty/ has any untracked files"""

        if self._repo is None:
            return True

        return self._repo.is_dirty() or bool(self._repo.untracked_files)


    def get_current_commit(self) -> str:
        """Get the commit hash of the current git repo"""

        if self._repo is None:
            return ""

        return self._repo.active_branch.commit.hexsha

    def get_base_dir(self) -> str:
        """Get the commit hash of the current git repo"""

        if self._repo is None:
            return ""

        return Path(self._repo.git_dir).parent.as_posix()
