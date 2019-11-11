import sys
import unittest
import coverage
import os

from flask.cli import FlaskGroup

from project import create_app
from project.api.cert_gen import EasyRSA

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py'
    ]
)
COV.start()
app = create_app()
cli = FlaskGroup(create_app = create_app)

@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)

@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)

@cli.command('create_folders')
def create_folders():
    """Creates de folders to store .crt files and .ovpn files"""
    ovpn_folder = app.config['OVPN_CERTS_PATH']
    crt_folder = app.config['CRT_CERTS_PATH']
    os.mkdir(ovpn_folder)
    os.mkdir(crt_folder)

@cli.command('start')
def start():
    """
    Creates all the necessary folders and files for the 
    service to run properly
    """
    ovpn_folder = app.config['OVPN_CERTS_PATH']
    crt_folder = app.config['CRT_CERTS_PATH']
    pki_path = app.config['PKI_PATH']
    if not os.path.isdir(ovpn_folder):
        os.mkdir(ovpn_folder)
    if not os.path.isdir(crt_folder):
        os.mkdir(crt_folder)
    if not os.path.isdir(pki_path):
        EasyRSA().init_pki()

if __name__ == "__main__":
    cli()
