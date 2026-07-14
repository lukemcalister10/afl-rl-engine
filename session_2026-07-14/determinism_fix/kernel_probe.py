#!/usr/bin/env python3
"""Print the OpenBLAS kernel numpy ACTUALLY resolved to, from numpy's own loaded .so.
CRITICAL: any OPENBLAS_CORETYPE / OPENBLAS_NUM_THREADS must be set in the ENV BEFORE this
runs (before numpy import). This queries the live handle, not a build-time label."""
import ctypes, os, sys
import numpy  # noqa  -- forces the .so to be loaded/resolved
# numpy 2.x bundles libscipy_openblas64_-<hash>.so with the scipy_openblas64_ symbol prefix.
import glob
np_libs = os.path.join(os.path.dirname(os.path.dirname(numpy.__file__)), 'numpy.libs')
so = glob.glob(os.path.join(np_libs, '*openblas*.so*'))
core = '?'
cfg = '?'
if so:
    lib = ctypes.CDLL(so[0])
    for cn, cc in (('scipy_openblas_get_corename64_', 'scipy_openblas_get_config64_'),
                   ('scipy_openblas64_get_corename', 'scipy_openblas64_get_config'),
                   ('openblas_get_corename64_', 'openblas_get_config64_'),
                   ('openblas_get_corename', 'openblas_get_config')):
        fn = getattr(lib, cn, None)
        if fn:
            fn.restype = ctypes.c_char_p
            core = fn().decode()
            cf = getattr(lib, cc, None)
            if cf:
                cf.restype = ctypes.c_char_p
                cfg = cf().decode()
            break
print("OPENBLAS_CORETYPE(env) =", os.environ.get('OPENBLAS_CORETYPE', '<unset>'),
      "| OPENBLAS_NUM_THREADS(env) =", os.environ.get('OPENBLAS_NUM_THREADS', '<unset>'))
print("RESOLVED KERNEL       =", core)
print("CONFIG                =", cfg)
