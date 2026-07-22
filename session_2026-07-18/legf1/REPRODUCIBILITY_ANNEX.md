# LEG F1 — REPRODUCIBILITY ANNEX (supervisor item 347)
captured: this session, container of record for the container-relative Leg-F proofs

## Python / numeric stack
python  : 3.12.3
numpy   : 2.4.4
scipy   : 1.17.1
sklearn : 1.8.0

## OpenBLAS (numpy.show_config -> blas)
      "blas": {
        "name": "scipy-openblas",
        "found": true,
        "version": "0.3.31.188.0",
        "detection method": "pkgconfig",
        "include directory": "/opt/_internal/cpython-3.12.12/lib/python3.12/site-packages/scipy_openblas64/include",
        "lib directory": "/opt/_internal/cpython-3.12.12/lib/python3.12/site-packages/scipy_openblas64/lib",

## Thread / BLAS env (the reconciliation surface)
  OPENBLAS_CORETYPE=<unset>
  OPENBLAS_NUM_THREADS=<unset>
  OMP_NUM_THREADS=<unset>
  MKL_NUM_THREADS=<unset>
  NUMEXPR_NUM_THREADS=<unset>
  PYTHONHASHSEED=<unset>
  (build recipe pins PYTHONHASHSEED=0; no CORETYPE pin — DYNAMIC_ARCH dispatches by CPU at runtime)

## lscpu (model + flags governing the SIMD kernel DYNAMIC_ARCH selects)
  Architecture:                            x86_64
  CPU(s):                                  4
  Model name:                              Intel(R) Xeon(R) Processor @ 2.80GHz
  Flags:                                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic

## The finding, one line
  store 968de0c7 + curve 56dd7a7b + engine files are byte-identical to the directive; the board-md5
  gap (30d96f1f vs filed 06d8af60, etc.) is OpenBLAS DYNAMIC_ARCH last-ULP weather confined to 6-dp
  float display fields. Integer v (valuation+ranking) is bit-identical to the filed panel: 10/10, 0 moves.
