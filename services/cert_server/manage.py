import sys
import unittest
import coverage
import os

from flask.cli import FlaskGroup

from project import create_app
from project.api.cert_manage import create_ca, transfer_crt

from shutil import rmtree

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

@cli.command('build_ca')
def build_ca():
    """Creates ca.crt and sends it to ovpn-server"""
    resp = create_ca()
    print(f'Creating ca certificate \n {resp}')

@cli.command('set_server_crt')
def set_server_crt():
    """Transfers server.crt to ovpn-server"""
    resp, stat = transfer_crt('server')
    print(f'{resp}, {stat}')

@cli.command('flush_certs')
def flush_certs():
    """Remove all certificates"""
    pki_path = app.config['PKI_PATH']
    if os.path.isdir(pki_path):
        print(f'removing {pki_path}')
        rmtree(pki_path)

if __name__ == "__main__":
    cli()
