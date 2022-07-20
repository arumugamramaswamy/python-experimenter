"""Module containing code used for managing configs"""
import copy
from logging import getLogger

from .exceptions import FrozenConfigException

logger = getLogger(__name__)


class ConfigNode(dict):
    """Create a config node with a similar constructor to dict()

    Args:
        dict_like: (Optional) Iterable/ mapping that can be converted to a dict

    Keyword only args:
        TBD

    Kwargs: keys that can be added to the dictionary using dict(key1=1)
    """

    FROZEN = "__frozen__"

    def __init__(self, dict_like=None, **kwargs):

        if dict_like is not None:
            internal_dict = dict(dict_like)
            for key, val in internal_dict.items():
                if isinstance(val, dict):
                    internal_dict[key] = ConfigNode(val)

            super().__init__(internal_dict, **kwargs)
        else:
            super().__init__(**kwargs)

        self.__dict__[ConfigNode.FROZEN] = False

    def freeze(self):
        """Make the ConfigNode immutable recursively

        Prevent further modifications to the ConfigNode until unfreeze is called
        """
        if self.is_frozen():
            logger.info("Already frozen")

        self.__dict__[ConfigNode.FROZEN] = True

        for value in self.values():
            if isinstance(value, ConfigNode):
                value.freeze()

    def unfreeze(self):
        """Return mutability to the ConfigNode recursively"""
        if not self.is_frozen():
            logger.info("Already not frozen")

        self.__dict__[ConfigNode.FROZEN] = False

        for value in self.values():
            if isinstance(value, ConfigNode):
                value.unfreeze()

    def is_frozen(self) -> bool:
        return self.__dict__[ConfigNode.FROZEN]

    def __setattr__(self, key, value):

        if self.is_frozen():
            raise FrozenConfigException(
                f"Cannot set {key} to {value} when ConfigNode is frozen. Call ConfigNode.unfreeze() to mutate ConfigNode"
            )

        assert (
            key not in self.__dict__
        ), f"Cannot set {key} which is a reserved attribute"

        self[key] = value

    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            raise AttributeError

    def update(self, _):
        raise NotImplementedError(
            "ConfigNode does not support update(), use the merge() function instead"
        )

    def merge(self, other_config: "ConfigNode"):
        """Merge other_config into this ConfigNode, overwritting with other_config when conflicts arise.

        A clone of other_config is used to update the current ConfigNode
        """

        if self.is_frozen():
            raise FrozenConfigException(
                "Cannot merge() when ConfigNode is frozen. Call ConfigNode.unfreeze() to mutate ConfigNode"
            )

        for key, value in other_config.clone().items():
            self[key] = value

    def clone(self) -> "ConfigNode":
        """Create a copy of the current ConfigNode"""
        return copy.deepcopy(self)

    def json_dump(self, path):
        """Dump the ConfigNode to a json file"""

        # import here to skip unnecessary imports at the top of the file
        import json

        with open(path, "w") as f:
            json.dump(self, f)

    @staticmethod
    def json_load(path) -> "ConfigNode":
        """Load ConfigNode from a json file"""

        # import here to skip unnecessary imports at the top of the file
        import json

        with open(path, "r") as f:
            d = json.load(f)

        return ConfigNode(d)

    def yaml_dump(self, path):
        """Dump the ConfigNode to a yaml file"""

        # import here to skip unnecessary imports at the top of the file
        import yaml

        with open(path, "w") as f:
            yaml.dump(self.to_dict(), f, Dumper=yaml.Dumper)

    @staticmethod
    def yaml_load(path) -> "ConfigNode":
        """Load ConfigNode from a yaml file"""

        # import here to skip unnecessary imports at the top of the file
        import yaml

        with open(path, "r") as f:
            d = yaml.load(f, Loader=yaml.Loader)

        return ConfigNode(d)

    def toml_dump(self, path):
        """Dump the ConfigNode to a toml file"""

        # import here to skip unnecessary imports at the top of the file
        import toml

        with open(path, "w") as f:
            toml.dump(self, f)

    @staticmethod
    def toml_load(path) -> "ConfigNode":
        """Load ConfigNode from a toml file"""

        # import here to skip unnecessary imports at the top of the file
        import toml

        with open(path, "r") as f:
            d = toml.load(f)

        return ConfigNode(d)

    def to_dict(self) -> dict:
        """Convert the ConfigNode object recursively to a dictionary"""
        output = {}

        for key, val in self.items():
            if isinstance(val, ConfigNode):
                output[key] = val.to_dict()
            else:
                output[key] = val

        return output
