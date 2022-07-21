import experimenter.git_utils
from unittest import mock

import unittest

class TestGitRepo(unittest.TestCase):

    @mock.patch("experimenter.git_utils.Repo")
    def test_is_clean(self, mock_repo):
        instance = mock_repo.return_value
        type(instance).untracked_files = mock.PropertyMock(return_value=[])
        instance.is_dirty.return_value = False

        a = experimenter.git_utils.GitRepo()

        assert not a.is_dirty()

    @mock.patch("experimenter.git_utils.Repo")
    def test_is_dirty_git_repo(self, mock_repo):
        instance = mock_repo.return_value
        type(instance).untracked_files = mock.PropertyMock(return_value=[])
        instance.is_dirty.return_value = True

        a = experimenter.git_utils.GitRepo()

        assert a.is_dirty()

    @mock.patch("experimenter.git_utils.Repo")
    def test_is_dirty_untracked_files(self, mock_repo):
        instance = mock_repo.return_value
        type(instance).untracked_files = mock.PropertyMock(return_value=["asdf/a"])
        instance.is_dirty.return_value = False

        a = experimenter.git_utils.GitRepo()

        assert a.is_dirty()
