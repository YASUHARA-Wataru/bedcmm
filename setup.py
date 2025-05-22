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
])

setup(
    name="bedcmm",
    version="0.1.0",
    author="WATARU YASUHARA",
    description="公開特許ベースのパターン抽出・通信多重化アルゴリズム",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YASUHARA-Wataru/bedcmm",
    packages=["bedcmm", "bedcmm.pattern", "bedcmm.communication"],
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    install_requires=[
        "cython",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.7',
)
