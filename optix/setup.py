# Copyright (c) 2022 NVIDIA CORPORATION All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import re
import sys
import platform
import subprocess
import shlex
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from packaging.version import parse as parse_version


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: " +
                ", ".join(e.name for e in self.extensions)
            )

        if platform.system() == "Windows":
            cmake_version_match = re.search(r'version\s*([\d.]+)', out.decode())
            if cmake_version_match:
                cmake_version = parse_version(cmake_version_match.group(1))
                if cmake_version < parse_version('3.1.0'):
                    raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = Path(self.get_ext_fullpath(ext.name)).parent.resolve()

        cmake_args = [
            f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}',
            f'-DPYTHON_EXECUTABLE={sys.executable}'
        ]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += [f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}']
            if sys.maxsize > 2 ** 32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += [f'-DCMAKE_BUILD_TYPE={cfg}']
            build_args += ['--', '-j']

        if "PYOPTIX_CMAKE_ARGS" in os.environ:
            cmake_args += shlex.split(os.environ['PYOPTIX_CMAKE_ARGS'])

        if "PYOPTIX_STDDEF_DIR" in os.environ:
            cmake_args += [f"-DOptiX_STDDEF_DIR={os.environ['PYOPTIX_STDDEF_DIR']}"]

        env = os.environ.copy()
        env['CXXFLAGS'] = f"{env.get('CXXFLAGS', '')} -DVERSION_INFO=\"{self.distribution.get_version()}\""

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        config_command = ['cmake', ext.sourcedir] + cmake_args
        print(f"CMAKE CMD: <<<{shlex.join(config_command)}>>>")

        subprocess.check_call(config_command, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)


setup(
    name='optix',
    version='0.1.0',
    author='Keith Morley, AtiDev17',
    author_email='kmorley@nvidia.com',
    description='Python bindings for NVIDIA OptiX',
    long_description='',
    ext_modules=[CMakeExtension('optix')],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
)