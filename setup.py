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


from setuptools import setup, Extension, find_packages
from distutils.command.build import build
from setuptools.command.install import install
# from setuptools.command.install_lib import install_lib

class CustomBuild(build):
    def run(self):
        self.run_command('build_ext')
        build.run(self)


class CustomInstall(install):
    def run(self):
        self.run_command('build_ext')
        self.do_egg_install()


setup(
    name='swiglpk',
    version='0.0.0',
    author='Nikolaus Sonnenschein',
    author_email='niko.sonnenschein@gmail.com',
    description='swiglpk - swig bindings for glpk',
    license='Apache License Version 2.0',
    keywords='optimization swig glpk',
    url='TBD',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: Apache Software License',
    ],
    py_modules=['swiglpk'],
    cmdclass={'build': CustomBuild, 'install': CustomInstall},
    ext_modules=[Extension("_swiglpk", sources=["glpk.i"], libraries=['glpk'])]
)