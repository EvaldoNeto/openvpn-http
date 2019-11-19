import sys
import unittest
import coverage
import os

from flask.cli import FlaskGroup

from project import create_app
from project.api.cert_gen import EasyRSA
from project.api.cert_manage import create_server

from shutil import copy2, rmtree

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

@cli.command('set_env')
def set_env():
    """
    Creates all the necessary folders and files for the 
    service to run properly
    """
    ovpn_folder = app.config['OVPN_CERTS_PATH']
    crt_folder = app.config['CRT_CERTS_PATH']
    pki_path = app.config['PKI_PATH']
    if not os.path.isdir(ovpn_folder):
        print(f'creating {ovpn_folder}')
        os.mkdir(ovpn_folder)
    if not os.path.isdir(crt_folder):
        print(f'creating {crt_folder}')
        os.mkdir(crt_folder)
    if not os.path.isdir(pki_path):
        print('initializing pki')
        EasyRSA().init_pki()

@cli.command('create_server_cert')
def create_server_cert():
    resp = create_server()
    print(f'Creating ca certificate \n {resp}')

@cli.command('conf_ovpn_server')
def conf_ovpn_server():
    """Set all necessarie files to /etc/ovpn """
    crt_folder = app.config['CRT_CERTS_PATH']
    pki_path = app.config['PKI_PATH']
    ovpn_path = app.config['OPENVPN']
    if not os.path.isfile(f'{crt_folder}/ca.crt'):
        print('ca.crt not found, please create it')
        return
    if not os.path.isfile(f'{crt_folder}/server.crt'):
        print('server.crt not found, please create it')
        return
    if not os.path.isfile(f'{pki_path}/dh.pem'):
        print('dh.pem not found, please create it')
        return
    if not os.path.isfile(f'{pki_path}/private/server.key'):
        print('server.key not found, please create it')
        return
    print(f'copying ca.crt, server.crt, dh.pem and server.key to {ovpn_path}')
    copy2(f'{crt_folder}/ca.crt', ovpn_path)
    copy2(f'{crt_folder}/server.crt', ovpn_path)
    copy2(f'{pki}/dh.pem', ovpn_path)
    copy2(f'{pki}/private/server.key', ovpn_path)

@cli.command('flush_certs')
def flush_certs():
    """Remove all certificates"""
    crt_folder = app.config['CRT_CERTS_PATH']
    pki_path = app.config['PKI_PATH']
    ovpn_path = app.config['OVPN_CERTS_PATH']
    if os.path.isdir(crt_folder):
        print(f'removing {crt_folder}')
        rmtree(crt_folder)
    if os.path.isdir(pki_path):
        print(f'removing {pki_path}')
        rmtree(pki_path)
    if os.path.isdir(ovpn_path):
        print(f'removing {ovpn_path}')
        rmtree(ovpn_path)

if __name__ == "__main__":
    cli()
