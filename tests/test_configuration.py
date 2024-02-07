import json
import unittest
from tempfile import TemporaryFile

from bsb import config
from bsb.config import Configuration, from_json
from bsb.core import Scaffold
from bsb.exceptions import ConfigurationWarning
from bsb_test import RandomStorageFixture, get_test_config_tree, get_test_config


def as_json(name: str):
    import json

    return json.dumps(get_test_config_tree(name))


class TestConfiguration(
    RandomStorageFixture, unittest.TestCase, setup_cls=True, engine_name="hdf5"
):
    def test_default_bootstrap(self):
        cfg = config.Configuration.default()
        Scaffold(cfg, self.storage)

    def test_json_minimal_bootstrap(self):
        with TemporaryFile(mode="w+") as f:
            f.write(as_json("minimal"))
            f.seek(0)
            config = from_json(f)
        Scaffold(config, self.storage)

    def test_json_minimal_content_bootstrap(self):
        config = from_json(data=as_json("minimal"))
        Scaffold(config, self.storage)

    def test_json_full_bootstrap(self):
        with TemporaryFile(mode="w+") as f:
            f.write(as_json("full_compile"))
            f.seek(0)
            config = from_json(f)
        Scaffold(config, self.storage)

    @unittest.expectedFailure
    def test_full_bijective(self):
        self.bijective("full_compile", Configuration, get_test_config_tree("full_compile"))

    def bijective(self, name, cls, tree):
        # Test that the tree and its config projection are the same in JSON
        with self.subTest(name=name):
            cfg = cls(tree)
            new_tree = cfg.__tree__()
            self.assertEqual(json.dumps(tree, indent=2), json.dumps(new_tree, indent=2))
            return cfg, new_tree
