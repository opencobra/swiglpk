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

import os
from setuptools import setup, Extension
import subprocess
import versioneer

def copy_glpk_header():
    if os.path.isfile('glpk.h'):
        print('glpk.h found in source directory')
        glpk_header_path = os.path.join('./', 'glpk.h')
    else:
        print('Trying to determine glpk.h location')
        glpsol_path = os.path.dirname(subprocess.check_output(['which', 'glpsol']))
        glpk_header_path = os.path.join(os.path.dirname(glpsol_path).decode("utf-8"), 'include', 'glpk.h')
        print('glpk.h found at {}'.format(glpk_header_path))
    if os.path.exists(glpk_header_path):
        with open('glpk_clean.h', 'w') as out_handle:
            with open(glpk_header_path) as in_handle:
                for line in in_handle:
                    if line == 'void glp_vprintf(const char *fmt, va_list arg);\n':
                        out_handle.write('// The following line is commented out because it is causing problems with swig\n')
                        out_handle.write('// void glp_vprintf(const char *fmt, va_list arg);')
                    else:
                        out_handle.write(line)
    else:
        raise Exception('Could not find glpk.h! Maybe glpk or glpsol is not installed.')


# Copy and process glpk.h into current directory
copy_glpk_header()

# from https://coderwall.com/p/qawuyq
try:
    import pypandoc

    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description = ''


custom_cmd_class = versioneer.get_cmdclass()

if os.name != 'nt':
    from distutils.command.build import build
    try:
        from wheel.bdist_wheel import bdist_wheel

        class CustomBdistWheel(bdist_wheel):
            def run(self):
                self.run_command('build_ext')
                bdist_wheel.run(self)

        custom_cmd_class['bdist_wheel'] = CustomBdistWheel
    except ImportError:
        pass  # custom command not needed if wheel is not installed

    class CustomBuild(build):
        def run(self):
            self.run_command('build_ext')
            build.run(self)

    custom_cmd_class['build'] = CustomBuild

setup(
    name='swiglpk',
    version=versioneer.get_version(),
    cmdclass=custom_cmd_class,
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
    ext_modules=[Extension("_swiglpk", sources=["glpk.i"], libraries=['glpk'])],
    include_package_data = True
)