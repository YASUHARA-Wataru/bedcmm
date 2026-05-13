from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
import numpy

ext_modules = cythonize([
    Extension(
        "bedcmm.pattern.cy_impl",  # bedcmm/pattern/cy_impl.pyx
        ["bedcmm/pattern/cy_impl.pyx"],
        include_dirs=[numpy.get_include()],
        language="c"
    )
], compiler_directives={'language_level': "3"})

setup(
    packages=["bedcmm", "bedcmm.pattern", "bedcmm.communication"],
    include_package_data=False,
    ext_modules=ext_modules,
)
