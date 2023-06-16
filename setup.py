from setuptools import setup
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]

setup(
    name='quebra_frases',
    version='0.3.7',
    packages=['quebra_frases'],
    url='https://github.com/OpenJarbas/quebra_frases',
    install_requires=required("requirements.txt"),
    license='apache-2.0',
    author='jarbasAi',
    author_email='jarbasai@mailfence.com',
    description='quebra_frases chunks strings into byte sized pieces'
)
