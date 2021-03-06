# -*- coding: utf-8 -*-
# Copyright 2014 - 2016 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
from os import mkdir
from os.path import abspath, isdir, join

import yaml

from synapse.config import find_config_files

from .config import create_config
from .constants import CONFIG_LOCK, DATA_SUBDIR
from .errors import BaseConfigInUseError
from .util import is_subpath


class Model:
    """
    The Model brokers modification of the config file and signing keys in the
    config directory.
    """

    def __init__(self, config_dir):
        self.config_dir = abspath(config_dir)
        self.data_dir = abspath(join(self.config_dir, DATA_SUBDIR))
        if not isdir(self.config_dir):
            mkdir(self.config_dir)

        if not isdir(self.data_dir):
            mkdir(self.data_dir)

    def get_config(self, config_path: str) -> dict:
        """
        Retrieves a config from the config directory. Any path can be provided
        but it must be a subdirectory of self.config_dir

        Args:
            config_path: path to the config

        Returns:
            The yaml parse of the config file
        """
        conf_path = abspath(join(self.config_dir, config_path))

        if not is_subpath(self.config_dir, conf_path):
            raise FileNotFoundError()

        with open(conf_path, "r") as f:
            return yaml.safe_load(f)

    def write_config(self, config: dict):
        """
        Given a config generates a templated config from synapse and writes it
        out to the config dir. It will raise an exception if the config in
        the config directory is in use.

        Args:
            config (dict): The configuration to template out.
        """
        if self.config_in_use():
            raise BaseConfigInUseError()

        for conf_name, conf in create_config(
            self.config_dir, self.data_dir, config
        ).items():
            with open(abspath(join(self.config_dir, conf_name)), "w") as f:
                f.write(conf)

    def config_in_use(self) -> bool:
        """
        Checks if we set whether the config is in use. If it was set up by the
        system but synapse wasn't launched yet we will have set this to False.
        However if it's not present we assume someone else has set up synapse
        before so we assume the config is in use.
        """
        config = {}
        config_files = find_config_files([self.config_dir])
        for config_file in config_files:
            with open(config_file) as stream:
                config.update(yaml.safe_load(stream))

        if not config:
            return False

        print(config.get(CONFIG_LOCK))
        return config.get(CONFIG_LOCK, True)

    def generate_secret_key(self, server_name: str) -> str:
        """
        Generates and writes a secret key.
        Args:
            server_name: The name of the homeserver

        Returns:
            The secret key identifying the server.
        """
        if self.config_in_use():
            raise BaseConfigInUseError()

        signing_key_path = join(self.config_dir, server_name + ".signing.key")
        subprocess.run(["generate_signing_key.py", "-o", signing_key_path])
        with open(signing_key_path, "r") as f:
            return f.read()
