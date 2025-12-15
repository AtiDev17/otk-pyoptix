# PyOptiX

Python bindings for OptiX 9.

## Installation


### Dependencies

#### OptiX SDK
Install [OptiX SDK](https://developer.nvidia.com/designworks/optix/download) version 9.1.

#### CUDA SDK
Install [CUDA SDK](https://developer.nvidia.com/cuda-downloads) version 13.1 is required.

#### Build system requirements:
* [cmake](https://cmake.org/)
* [pip](https://pypi.org/project/pip/)

#### Code sample dependencies
To run the PyOptiX examples or tests, the python modules specified in `PyOptiX/requirements.txt` must be installed:
* pytest
* cupy
* numpy
* Pillow
* cuda-python 

### Virtual Environment
In most cases, it makes sense to setup a python environment. Below are examples of how to setup your environment via either`Conda` or `venv`.

#### `venv` Virtual Environment
Create and activate a new virtual environment:
```
python3 -m venv env
source env/bin/activate
```
Install all dependencies:
```
pip install -r requirements.txt
```

#### Conda Environment
Create an environment containing pre-requisites:
```
conda create -n pyoptix python numpy conda-forge::cupy pillow pytest
```
Activate the environment:
```
conda activate pyoptix
```
The `pynvrtc` dependency, necessary for running the examples, needs to be installed via pip:
```
pip install pynvrtc
```

### Building and installing the `optix` Python module

The build system automatically attempts to locate the latest OptiX SDK installation in standard system directories (e.g., `C:\ProgramData\NVIDIA Corporation\OptiX SDK *` on Windows or `/opt/nvidia/optix*` on Linux).

Build and install using `pip` and `setuptools.py`:
```
cd optix
pip install .
```

#### Manual Configuration (Optional)
If the auto-detection fails or you installed the SDK in a non-standard location, you can point `setuptools/CMake` to your OptiX installation by setting the `PYOPTIX_CMAKE_ARGS` environment variable.

Linux:
```
export PYOPTIX_CMAKE_ARGS="-DOptiX_INSTALL_DIR=<optix install dir>"
```
Windows:
```
set PYOPTIX_CMAKE_ARGS=-DOptiX_INSTALL_DIR=C:\ProgramData\NVIDIA Corporation\OptiX SDK 9.1.0
```

When compiling against an Optix 7.0 SDK an additional environment variable needs to be set
containing a path to the system's stddef.h location. E.g.
```
export PYOPTIX_STDDEF_DIR="/usr/include/linux"
```

## Running the Examples

Run the `hello` sample:
```
cd examples
python hello.py
```
If the example runs successfully, a green square will be rendered.

## Running the Test Suite

Test tests are using `pytest` and can be run from the test directory like this:
```
cd test
python -m pytest
```
