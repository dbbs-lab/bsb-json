import json
import unittest

from bsb import config
from bsb.config import from_json, Configuration
from bsb.core import Scaffold
from bsb.exceptions import ConfigurationWarning
from bsb_test import RandomStorageFixture, get_config_path

minimal_config = get_config_path("test_minimal.json")
full_config = get_config_path("test_core.json")


def as_json(f):
    import json

    with open(f, "r") as fh:
        return json.load(fh)


class TestConfiguration(
    RandomStorageFixture, unittest.TestCase, setup_cls=True, engine_name="hdf5"
):
    def test_default_bootstrap(self):
        cfg = config.Configuration.default()
        Scaffold(cfg, self.storage)

    def test_json_minimal_bootstrap(self):
        config = from_json(minimal_config)
        Scaffold(config, self.storage)

    def test_json_minimal_content_bootstrap(self):
        with open(minimal_config, "r") as f:
            content = f.read()
        config = from_json(data=content)
        Scaffold(config, self.storage)

    def test_json_full_bootstrap(self):
        config = from_json(full_config)
        Scaffold(config, self.storage)

    def test_json_full_no_unknown_attributes(self):
        try:
            with self.assertWarns(ConfigurationWarning) as cm:
                from_json(full_config)
            self.fail(f"Unknown configuration attributes detected: {cm.warning}")
        except AssertionError:
            pass

    @unittest.expectedFailure
    def test_full_bijective(self):
        self.bijective("full", Configuration, as_json(full_config))

    def bijective(self, name, cls, tree):
        # Test that the tree and its config projection are the same in JSON
        with self.subTest(name=name):
            cfg = cls(tree)
            new_tree = cfg.__tree__()
            self.assertEqual(json.dumps(tree, indent=2), json.dumps(new_tree, indent=2))
            return cfg, new_tree