#!/usr/bin/env python3
# ci-env-pin E2 helper — print the RESOLVED OpenBLAS kernel + thread count for THIS process, so a build's
# forced OPENBLAS_CORETYPE / OPENBLAS_NUM_THREADS is PROVEN to have taken effect (a mis-typed coretype is
# silently ignored by OpenBLAS, which would make a forced run look identical to baseline for the wrong reason).
import numpy as _np
_np.dot(_np.ones((8, 8)), _np.ones((8, 8)))  # force the BLAS library to actually load before probing
try:
    from threadpoolctl import threadpool_info
    ob = [x for x in threadpool_info() if x.get("internal_api") == "openblas"]
    if ob:
        print("resolved: arch=%s threads=%s" % (ob[0].get("architecture"), ob[0].get("num_threads")))
    else:
        print("resolved: arch=? threads=? (no openblas layer found)")
except Exception as e:
    print("resolved: probe-err", e)
