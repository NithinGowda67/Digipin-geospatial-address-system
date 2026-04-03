"""
Setup script for digipinpy with optional Cython acceleration.

This setup.py enables building Cython extensions for 10-15x performance improvement.
Falls back gracefully to pure Python if Cython is not available.

Building with Cython:
    pip install cython  # Install Cython first
    python setup.py build_ext --inplace  # Compile extensions
    pip install -e .  # Install in development mode

Building binary wheels:
    pip install cython wheel
    python setup.py bdist_wheel  # Creates platform-specific wheel
"""

import sys
from pathlib import Path
from setuptools import setup, Extension

# Determine if Cython is available
try:
    from Cython.Build import cythonize
    USE_CYTHON = True
    print("Cython found - building optimized extensions")
except ImportError:
    USE_CYTHON = False
    print("WARNING: Cython not found - skipping performance extensions")
    print("  Install Cython for 10-15x speedup: pip install cython")

# Configure Cython extension
extensions = []

if USE_CYTHON:
    # Cython extension configuration
    # Platform-specific compiler flags
    if sys.platform == "win32":
        # Windows MSVC compiler flags
        extra_compile_args = ["/O2"]
    elif sys.platform == "darwin":
        # macOS: Use conservative flags (no -march=native for ARM/Intel compatibility)
        extra_compile_args = ["-O3"]
    else:
        # Linux: Safe optimization flags
        extra_compile_args = ["-O3"]

    ext_module = Extension(
        name="digipin.core_fast",
        sources=["src/digipin/core_fast.pyx"],
        language="c",
        extra_compile_args=extra_compile_args,
    )

    # Cythonize with compiler directives
    try:
        extensions = cythonize(
            [ext_module],
            compiler_directives={
                "language_level": "3",  # Python 3 syntax
                "boundscheck": False,  # Disable bounds checking for speed
                "wraparound": False,  # Disable negative indexing
                "cdivision": True,  # Use C division (faster)
                "embedsignature": True,  # Embed function signatures for help()
            },
            # Annotate HTML for performance analysis (optional)
            annotate=False,
        )
    except Exception as e:
        print(f"WARNING: Cython compilation setup failed: {e}")
        print("  Falling back to pure Python (no performance extensions)")
        extensions = []
        USE_CYTHON = False

# Call setup with extensions (if available)
# Use try-except to gracefully handle compilation failures during install
try:
    setup(
        ext_modules=extensions,
        # All other metadata read from pyproject.toml
    )
except Exception as e:
    # If compilation fails during setup, retry without extensions
    if extensions:
        print(f"\nWARNING: C extension compilation failed: {e}")
        print("  Installing package with pure Python implementation only")
        print("  Performance will be reduced but functionality is identical\n")
        setup(
            ext_modules=[],
            # All other metadata read from pyproject.toml
        )
    else:
        # If failure wasn't extension-related, re-raise
        raise
