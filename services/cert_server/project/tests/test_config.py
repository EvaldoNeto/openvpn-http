# services/cert_server/project/tests/test_config.py


import os
import unittest

from flask import current_app
from flask_testing import TestCase

from project import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] ==
                        os.environ.get('SECRET_KEY'))
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] ==
                        os.environ.get('SECRET_KEY'))
        self.assertTrue(app.config['TESTING'])


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['SECRET_KEY'] ==
                        os.environ.get('SECRET_KEY'))
        self.assertFalse(app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()
