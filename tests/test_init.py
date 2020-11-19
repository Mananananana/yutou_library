# todo: test __init__ file

import unittest

from werkzeug.exceptions import BadRequest
from flask import url_for

from tests.base import BaseTestCase
from yutou_library.libs.error_code import Success


class InitTestCase(BaseTestCase):
    def test_errors(self):
        @self.app.route("/httpexception")
        def func():
            return BadRequest()

        @self.app.route("/apiexception")
        def func2():
            return Success()

        @self.app.route("/normalexception")
        def func3():
            1/0
        response = self.client.get(url_for("func"))
        self.assertEqual(response.status_code, 400)
        response = self.client.get(url_for("func2"))
        self.assertEqual(response.status_code, 201)
        debug = self.app.config["DEBUG"]
        self.app.config["DEBUG"] = False
        response = self.client.get(url_for("func3"))
        self.assertEqual(response.status_code, 500)
        self.app.config["DEBUG"] = debug

    def test_initdb_command(self):
        result = self.runner.invoke(self.app.cli.commands["initdb"])
        self.assertIn("Create databases", result.output)

    def test_initdb_with_drop_command(self):
        result = self.runner.invoke(self.app.cli.commands["initdb"], ["--drop"], input="y\n")
        self.assertIn("This operation will drop the database, do you want to continue?", result.output)
        self.assertIn("Drop databases", result.output)


if __name__ == "__main__":
    unittest.main()
