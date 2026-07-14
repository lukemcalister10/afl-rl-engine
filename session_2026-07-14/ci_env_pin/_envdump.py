#!/usr/bin/env python3
# ci-env-pin E1 helper — dump the FULL numpy/BLAS environment (versions, show_config, the RESOLVED
# OpenBLAS kernel + thread count via threadpoolctl, and every BLAS/thread env var python actually sees).
# Diagnostic only. Run on both the runner and the pinned box; the outputs go side by side.
import numpy, scipy, sklearn, json, os
print("versions: numpy", numpy.__version__, "scipy", scipy.__version__, "sklearn", sklearn.__version__)
print("--- numpy.show_config() ---")
try:
    numpy.show_config()
except Exception as e:
    print("show_config err", e)
print("--- threadpoolctl (the RESOLVED kernel + thread count OpenBLAS ACTUALLY uses) ---")
try:
    from threadpoolctl import threadpool_info
    print(json.dumps(threadpool_info(), indent=1))
except Exception as e:
    print("threadpoolctl unavailable:", e)
print("--- os.environ BLAS/thread vars seen by python ---")
_hit = False
for k in sorted(os.environ):
    if any(k.startswith(p) for p in ("OPENBLAS", "OMP", "MKL", "NPY", "BLIS", "VECLIB", "NUMEXPR", "GOTO")):
        print(k, "=", os.environ[k]); _hit = True
if not _hit:
    print("(none set)")
