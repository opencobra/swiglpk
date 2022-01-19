# swiglpk - Swig Python bindings for the GNU Linear Programming Kit (GLPK)
# Copyright (C) 2015 The Novo Nordisk Foundation Center for Biosustainability
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# http://stackoverflow.com/questions/12491328/python-distutils-not-include-the-swig-generated-module

import os
import warnings
from distutils.core import setup, Extension
from distutils.command.build import build
import subprocess
import versioneer


ENV_GLPK_HEADER_PATH = 'GLPK_HEADER_PATH'
GLPK_HEADER_NAME = 'glpk.h'
GLPSOL_BINARY_NAME = 'glpsol'
INCLUDE_DIRS = (
    '/usr/local/include',
    '/usr/include',
    '/include',
)


class CustomBuild(build):
    sub_commands = [
        ('build_ext', build.has_ext_modules),
        ('build_py', build.has_pure_modules),
        ('build_clib', build.has_c_libraries),
        ('build_scripts', build.has_scripts),
    ]


def find_glpk_header():
    # If a path is provded by the environment, expect the GLPK header there.
    given_path = os.environ.get(ENV_GLPK_HEADER_PATH, None)
    if given_path:
        if os.path.isfile(given_path):
            if os.path.basename(given_path) == GLPK_HEADER_NAME:
                return os.path.abspath(os.path.dirname(given_path))
            else:
                warnings.warn(
                    'The environment variable {}="{}" points to a file not '
                    'named {}.'.format(ENV_GLPK_HEADER_PATH, given_path,
                    GLPK_HEADER_NAME), stacklevel=2
                )
        elif os.path.isdir(given_path):
            header = os.path.join(given_path, GLPK_HEADER_NAME)

            if os.path.isfile(header):
                return os.path.abspath(given_path)
            else:
                warnings.warn(
                    'The environment variable {}="{}" is set to a directory '
                    'that does not contain {}.'.format(ENV_GLPK_HEADER_PATH,
                    given_path, GLPK_HEADER_NAME), stacklevel=2
                )
        else:
            warnings.warn(
                'The environment variable {}="{}" does not point to a '
                'directory or file.'.format(ENV_GLPK_HEADER_PATH, given_path),
                stacklevel=2
            )

    # Look for a drop-in header file next.
    if os.path.isfile(GLPK_HEADER_NAME):
        return os.getcwd()

    include_dirs = list(INCLUDE_DIRS)

    # If glpsol is found, look for an include directory in its vicinity.
    try:
        from shutil import which
    except ImportError:  # Python < 3.3.
        pass
    else:
        glpsol = which(GLPSOL_BINARY_NAME)

        if glpsol:
            glpsol_path = os.path.dirname(glpsol)
            glpsol_root = os.path.dirname(glpsol_path)
            glpsol_include_path = os.path.join(glpsol_root, "include")
            include_dirs.insert(0, glpsol_include_path)

    # Look at common places.
    for path in include_dirs:
        if os.path.isdir(path):
            header = os.path.join(path, GLPK_HEADER_NAME)

            if os.path.isfile(header):
                return os.path.abspath(path)

    raise FileNotFoundError('Failed to locate {}.'.format(GLPK_HEADER_NAME))


# Warn users installing via pip that this is a source build.
print(
    '='*30,
    'BUILDING SWIGLPK FROM SOURCE.',
    'If you are installing SWIGLPK via pip, this means that no wheels are'
    ' offered for your platform or Python version yet.',
    'This can be the case if you adopt a new Python version early.',
    'A source build requires GLPK, SWIG, and GMP (Linux/Mac) to be installed!',
    '='*30,
    sep='\n'
)

# Find the GLPK header.
try:
    print('Looking for {}...'.format(GLPK_HEADER_NAME))

    glpk_header_dirname = find_glpk_header()
except FileNotFoundError as error:
    raise RuntimeError(
        'A source build of SWIGLPK requires GLPK to be installed but we could'
        ' not find {0}. You may put {0} inside the current directory or link'
        ' to its parent folder via {1}.'
        .format(GLPK_HEADER_NAME, ENV_GLPK_HEADER_PATH)
    ) from error
else:
    print('Found {} in {}.'.format(GLPK_HEADER_NAME, glpk_header_dirname))

# Make sure SWIG is available.
try:
    from shutil import which
except ImportError:
    pass  # This check is not critical given the warning above.
else:
    print('Making sure SWIG is available...')

    if which('swig'):
        print('Found the swig executable.')
    else:
        raise RuntimeError(
            'A source build of SWIGLPK requires SWIG to be installed but we '
            'could not find the swig executable.')

# Assemble custom_cmd_class.
custom_cmd_class = versioneer.get_cmdclass()
custom_cmd_class['build'] = CustomBuild

try:
    from wheel.bdist_wheel import bdist_wheel

    class CustomBdistWheel(bdist_wheel):
        def run(self):
            self.run_command('build_ext')
            bdist_wheel.run(self)

    custom_cmd_class['bdist_wheel'] = CustomBdistWheel
except ImportError:
    pass  # Custom command not needed if wheel is not installed.

# Read long description from README.rst.
try:
    with open('README.rst', 'r') as f:
        long_description = f.read()
except Exception:
    long_description = ''

# Run setup.
setup(
    name='swiglpk',
    version=versioneer.get_version(),
    cmdclass=custom_cmd_class,
    packages=['swiglpk'],
    package_dir={'swiglpk': 'swiglpk'},
    author='Nikolaus Sonnenschein',
    author_email='niko.sonnenschein@gmail.com',
    description='swiglpk - Simple swig bindings for the GNU Linear Programming Kit',
    license='GPL v3',
    keywords='optimization swig glpk',
    url='https://github.com/biosustain/swiglpk',
    long_description=long_description,
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    ext_modules=[
        Extension(
            "swiglpk._swiglpk",
            sources=["swiglpk/glpk.i"],
            include_dirs=[glpk_header_dirname],
            swig_opts=["-I"+glpk_header_dirname],
            libraries=['glpk'])
    ],
    include_package_data=True
)
