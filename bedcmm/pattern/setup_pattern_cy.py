from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension
import numpy
import os
from pathlib import Path

file_dir = Path(__file__).resolve().parent
extensions = [
    Extension("bedcmm.pattern.cy_impl", [os.path.join(file_dir,"cy_impl.pyx")],
        include_dirs=[numpy.get_include()])
]

setup(
    name="cy_impl",
    ext_modules=cythonize(extensions)
)
