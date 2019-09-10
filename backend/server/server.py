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

from os.path import abspath, dirname, join, isabs

from canonicaljson import json

from twisted.web.static import File

from klein import Klein

from .utils import port_checker
from model import constants
from .schemas import BASE_CONFIG_SCHEMA, CERTS_SCHEMA, PORTS_SCHEMA, SECRET_KEY_SCHEMA
from .utils import validate_schema


import subprocess


class Server:
    app = Klein()

    def __init__(self, model):
        self.model = model

    def server_webui(self, request):
        client_path = abspath(join(dirname(abspath(__file__)), "../../webui/dist/"))
        return File(client_path)

    app.route("/", branch=True)(server_webui)

    @app.route("/setup", methods=["GET"])
    def get_config_setup(self, request):
        return json.dumps(
            {
                constants.CONFIG_LOCK: self.model.config_in_use(),
                "config_dir": self.model.config_dir,
            }
        )

    @app.route("/secretkey", methods=["POST"])
    @validate_schema(SECRET_KEY_SCHEMA)
    def get_secret_key(self, request, body):
        return json.dumps(
            {"secret_key": self.model.generate_secret_key(body["server_name"])}
        )

    @app.route("/config", methods=["GET"])
    def get_config(self, request):
        return str(self.model.get_config())

    @app.route("/config", methods=["POST"])
    @validate_schema(BASE_CONFIG_SCHEMA)
    def set_config(self, request, body):
        self.model.write_config(body)

    @app.route("/testcertpaths", methods=["POST"])
    def test_cert_paths(self, request):
        body = json.loads(request.content.read())
        result = {}
        config_path = self.model.config_dir
        for name, path in body.items():
            if not isabs(path):
                path = abspath(join(config_path, path))
            try:
                with open(path, "r"):
                    result[name] = {"invalid": False, "absolute_path": path}
            except Exception:
                result[name] = {"invalid": True}
        return json.dumps(result)

    @app.route("/certs", methods=["POST"])
    @validate_schema(CERTS_SCHEMA)
    def upload_certs(self, request, body):
        self.model.add_certs(**body)

    @app.route("/ports", methods=["POST"])
    @validate_schema(PORTS_SCHEMA)
    def check_ports(self, request, body):
        results = []
        for port in body["ports"]:
            results.append(port_checker(port))
        return json.dumps({"ports": results})

    @app.route("/start", methods=["POST"])
    def start_synapse(self, request):
        print("Starting synapse")
        subprocess.check_output(["synctl", "start", self.model.config_dir])

    @app.route("/favicon.ico")
    def noop(self, request):
        return
