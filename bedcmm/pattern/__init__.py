import importlib
import warnings
import os
import subprocess
import sys
from pathlib import Path

generate_sequence = None
analyze_periodicity = None
implementation = "Unknown"

MODULE_DIR = Path(__file__).parent
CYTHON_MODULE_PATH = os.path.join(MODULE_DIR , "cy_impl*" + (".pyd" if os.name == "nt" else ".so"))

def build_cython_if_needed():
    """Cython拡張がビルドされていない場合、自動でビルドを試みる"""
    if not os.path.exists(CYTHON_MODULE_PATH):
        try:
            subprocess.run(
                [sys.executable, os.path.join(MODULE_DIR , "setup_pattern_cy.py"), "build_ext", "--inplace"],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            print("Cython build failed:\n", e.stderr.decode())

# Cythonのビルドを試みる
build_cython_if_needed()

# Cythonが読み込めるなら優先
try:
    cy_impl = importlib.import_module(".cy_impl", package=__name__)
    pattern_1d = cy_impl.pattern_1d
    pattern_2d = cy_impl.pattern_2d
    pattern_3d = cy_impl.pattern_3d
    periodicity_1d = cy_impl.periodicity_1d
    periodicity_2d = cy_impl.periodicity_2d
    periodicity_3d = cy_impl.periodicity_3d
    continuity_1d = cy_impl.continuity_1d
    continuity_2d = cy_impl.continuity_2d
    continuity_3d = cy_impl.continuity_3d
    implementation = "Cython"
except ImportError:
    print(ImportError)
    from .py_impl import pattern_1d,pattern_2d,pattern_3d,periodicity_1d,periodicity_2d,periodicity_3d,continuity_1d,continuity_2d,continuity_3d
    implementation = "Python"
    warnings.warn("Cython module not available. Falling back to pure Python.")

__all__ = ["pattern_1d", 
           "pattern_2d",
           "pattern_3d",
           "periodicity_1d",
           "periodicity_2d",
           "periodicity_3d",
           "continuity_1d",
           "continuity_2d",
           "continuity_3d",
           "implementation"]
