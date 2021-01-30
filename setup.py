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
from distutils.core import setup, Extension
from distutils.command.build import build
import re
import subprocess
import versioneer

EXCLUDE = [
    r'void glp_vprintf\(.+\);',
    # see https://lists.gnu.org/archive/html/bug-glpk/2021-01/msg00002.html
    r'void glp_netgen_prob\(.+\n*.+;',
]


def copy_glpk_header():
    if os.path.isfile('glpk.h'):
        print('glpk.h found in source directory')
        glpk_header_path = os.path.join('./', 'glpk.h')
    elif "GLPK_HEADER_PATH" in os.environ:
        glpk_header_path = os.path.join(os.environ["GLPK_HEADER_PATH"], 'glpk.h')
    else:
        print('Trying to determine glpk.h location')
        glpsol_path = os.path.dirname(subprocess.check_output(['which', 'glpsol']))
        glpk_header_path = os.path.join(os.path.dirname(glpsol_path).decode("utf-8"), 'include', 'glpk.h')
        print('glpk.h found at {}'.format(glpk_header_path))
    if os.path.exists(glpk_header_path):
        with open('swiglpk/glpk_clean.h', 'w') as out_handle:
            with open(glpk_header_path) as in_handle:
                content = in_handle.read()
                for ex in EXCLUDE:
                    content = re.sub(
                        ex,
                        "// This line was removed by swiglpk",
                        content)
                out_handle.write(content)
    else:
        raise Exception('Could not find glpk.h! Maybe glpk or glpsol is not installed.')


try:
    with open('README.rst', 'r') as f:
        long_description = f.read()
except Exception:
    long_description = ''


# Copy and process glpk.h into current directory
copy_glpk_header()

custom_cmd_class = versioneer.get_cmdclass()


class CustomBuild(build):
    sub_commands = [
        ('build_ext', build.has_ext_modules),
        ('build_py', build.has_pure_modules),
        ('build_clib', build.has_c_libraries),
        ('build_scripts', build.has_scripts),
    ]


custom_cmd_class['build'] = CustomBuild

try:
    from wheel.bdist_wheel import bdist_wheel

    class CustomBdistWheel(bdist_wheel):
        def run(self):
            self.run_command('build_ext')
            bdist_wheel.run(self)

    custom_cmd_class['bdist_wheel'] = CustomBdistWheel
except ImportError:
    pass  # custom command not needed if wheel is not installed

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
    ext_modules=[Extension("swiglpk._swiglpk",
                           sources=["swiglpk/glpk.i"],
                           libraries=['glpk'])],
    include_package_data=True
)
