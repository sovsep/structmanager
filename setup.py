from __future__ import absolute_import

import os
import inspect
import subprocess
from setuptools import setup, find_packages


is_released = True
version = '0.4.0'


def git_version():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        git_revision = out.strip().decode('ascii')
    except OSError:
        git_revision = "Unknown"

    return git_revision


def get_version_info(version, is_released):
    fullversion = version
    if not is_released:
        git_revision = git_version()
        fullversion += '.dev0+' + git_revision[:7]
    return fullversion


def write_version_py(version, is_released, filename='structmanager/version.py'):
    fullversion = get_version_info(version, is_released)
    with open("./structmanager/version.py", "wb") as f:
        f.write(b'__version__ = "%s"\n' % fullversion.encode())
    return fullversion


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    setupdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return open(os.path.join(setupdir, fname)).read()


#_____________________________________________________________________________

install_requires = [
        "numpy",
        "scipy",
        "coveralls",
        "pyNastran",
        "setuptools-git-version",
        ]

CLASSIFIERS = """\

Development Status :: 3 - Alpha
Intended Audience :: Science/Research
Intended Audience :: Developers
Intended Audience :: Education
Topic :: Scientific/Engineering :: Mathematics
License :: OSI Approved :: BSD License
Operating System :: Microsoft :: Windows
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.5
Operating System :: Unix

"""

fullversion = write_version_py(version, is_released)

data_files = [('', [
        'README.rst',
        'LICENSE',
        'structmanager/version.py',
        ])]

package_data = {
        '': ['tests/*.*'],
        }

s = setup(
    name = "structmanager",
    version = fullversion,
    author = "Saullo G. P. Castro",
    author_email = "castrosaullo@gmail.com",
    description = ("Structural Analysis Helper"),
    license = "BSD",
    keywords = "structural analysis; stress analysis; automation",
    url = "https://github.com/compmech/structmanager",
    packages=find_packages(),
    package_data=package_data,
    data_files=data_files,
    long_description=read('README.rst'),
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
    install_requires=install_requires,
)

