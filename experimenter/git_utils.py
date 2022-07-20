from git.repo.base import Repo
from git.exc import InvalidGitRepositoryError

import logging
import typing as T

logger = logging.getLogger(__name__)


def _get_repo() -> T.Optional[Repo]:
    try:
        return Repo()
    except InvalidGitRepositoryError:
        logger.warn("Could not find repo")
        return None

def is_repo_clean() -> bool:
    """Check if current repo is clean"""

    repo = _get_repo()
    if repo is None:
        return False

    return not repo.is_dirty() and not repo.untracked_files

def get_current_commit() -> str:
    """Get the commit hash of the current git repo"""

    repo = _get_repo()
    if repo is None:
        return ""

    return repo.active_branch.commit.hexsha

