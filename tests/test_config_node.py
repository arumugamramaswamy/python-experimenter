import unittest
import experimenter.config_node
import experimenter.exceptions
import tempfile


class TestConfigNode(unittest.TestCase):
    def test_freeze_config(self):
        cfg = experimenter.config_node.ConfigNode({"a": 1})
        cfg.freeze()

        with self.assertRaises(experimenter.exceptions.FrozenConfigException):
            cfg.b = 1

    def test_freeze_config_recursive(self):
        cfg = experimenter.config_node.ConfigNode({"a": {"b": 3}})
        cfg.freeze()

        with self.assertRaises(experimenter.exceptions.FrozenConfigException):
            cfg.a.b = 1

    def test_unfreeze_config(self):
        cfg = experimenter.config_node.ConfigNode({"a": 1})
        cfg.freeze()

        cfg.unfreeze()
        cfg.b = 1

    def test_unfreeze_config_recursive(self):
        cfg = experimenter.config_node.ConfigNode({"a": {"b": 3}})
        cfg.freeze()

        cfg.unfreeze()
        cfg.a.b = 1

    def test_dump_load_yaml(self):
        cfg = experimenter.config_node.ConfigNode({"a": {"b": 3}})
        with tempfile.NamedTemporaryFile() as f:
            cfg.yaml_dump(f.name)
            loaded = experimenter.config_node.ConfigNode.yaml_load(f.name)

        self.assertEqual(cfg, loaded)

    def test_dump_load_dict(self):
        cfg = experimenter.config_node.ConfigNode({"a": {"b": 3}})
        with tempfile.NamedTemporaryFile() as f:
            d = cfg.to_dict()
            loaded = experimenter.config_node.ConfigNode(d)

        self.assertEqual(cfg, loaded)
