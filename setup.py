# Copyright 2014 Novo Nordisk Foundation Center for Biosustainability, DTU.

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

import os
from setuptools import setup, Extension, find_packages
from distutils.command.build import build
from setuptools.command.install import install
import subprocess

def copy_glpk_header():
    glpsol_path = os.path.dirname(subprocess.check_output(['which', 'glpsol']))
    glpk_header_path = os.path.join(os.path.dirname(glpsol_path).decode("utf-8"), 'include', 'glpk.h')
    if os.path.exists(glpk_header_path):
        with open('glpk.h', 'w') as out_handle:
            with open(glpk_header_path) as in_handle:
                for line in in_handle:
                    if line == 'void glp_vprintf(const char *fmt, va_list arg);\n':
                        out_handle.write('// The following line is commented out because it is causing problems with swig\n')
                        out_handle.write('// void glp_vprintf(const char *fmt, va_list arg);')
                    else:
                        out_handle.write(line)
    else:
        raise Exception('Could not find glpk.h! Maybe glpk or glpsol is not installed.')


class CustomBuild(build):
    def run(self):
        self.run_command('build_ext')
        build.run(self)


class CustomInstall(install):
    def run(self):
        self.run_command('build_ext')
        self.do_egg_install()

# Copy and process glpk.h into current directory
copy_glpk_header()

# from https://coderwall.com/p/qawuyq
try:
    import pypandoc

    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description = ''

setup(
    name='swiglpk',
    version='1.0.0',
    author='Nikolaus Sonnenschein',
    author_email='niko.sonnenschein@gmail.com',
    description='swiglpk - Simple swig bindings for the GNU Linear Programming Kit',
    license='Apache License Version 2.0',
    keywords='optimization swig glpk',
    url='https://github.com/biosustain/swiglpk',
    long_description=description,
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: Apache Software License',
    ],
    py_modules=['swiglpk'],
    cmdclass={'build': CustomBuild, 'install': CustomInstall},
    ext_modules=[Extension("_swiglpk", sources=["glpk.i"], libraries=['glpk'])],
    include_package_data = True
)