#!/usr/bin/env python3
"""Shared EXTERNAL proof-output contract for the ITEM 408 sibling harnesses (register v432 note 6).

Ordinary proof runs must write their result JSON OUTSIDE the Git working tree, so no proof run mutates a
tracked byte (the register-v432 hygiene requirement). The contract:

  * ITEM408_PROOF_OUT=<absolute external directory>  overrides the default output directory;
  * with no override, a fresh external temporary directory is created;
  * an output directory INSIDE the harness's Git checkout is REJECTED fail-closed;
  * each harness writes a DISTINCT filename;
  * the result JSON is written ATOMICALLY (temp + os.replace);
  * the resolved external path is returned (the caller prints it);
  * a write failure raises (the caller must then exit non-zero).

This helper computes NO product value and edits NO tracked file; it only decides WHERE a result JSON goes.
"""
import json
import os
import subprocess
import tempfile


def _repo_root(start):
    """git toplevel of `start` (the tracked checkout the harness belongs to), or None if not a checkout."""
    try:
        r = subprocess.run(["git", "-C", start, "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True)
    except OSError:
        return None
    return os.path.realpath(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None


def _is_inside(path, root):
    p = os.path.realpath(path)
    return root is not None and (p == root or p.startswith(root + os.sep))


def resolve_out_dir(anchor):
    """Return an EXISTING external output directory for a harness whose file path is `anchor`.

    ITEM408_PROOF_OUT overrides the default. A path inside the harness's Git checkout is refused
    fail-closed (SystemExit). With no override, a fresh external temp directory is created."""
    repo = _repo_root(os.path.dirname(os.path.abspath(anchor)))
    env = os.environ.get("ITEM408_PROOF_OUT")
    if env:
        out = os.path.realpath(os.path.abspath(os.path.expanduser(env)))
        if _is_inside(out, repo):
            raise SystemExit(
                "ITEM408_PROOF_OUT=%s is INSIDE the Git checkout %s — refusing: proof outputs must not "
                "mutate tracked bytes (register v432 note 6). Point it at an external directory." % (out, repo))
        os.makedirs(out, exist_ok=True)
        return out
    out = tempfile.mkdtemp(prefix="item408-proof-out-")
    if _is_inside(out, repo):      # extremely defensive: TMPDIR should never be inside the repo
        raise SystemExit("default temp output %s resolved INSIDE the checkout %s — refusing" % (out, repo))
    return out


def write_result(anchor, filename, payload):
    """Atomically write `payload` (a dict) as JSON to <external out dir>/<filename>; return the full path.
    Fail-closed: any resolution/write error propagates so the caller exits non-zero."""
    out_dir = resolve_out_dir(anchor)
    dst = os.path.join(out_dir, filename)
    tmp = dst + ".tmp"
    with open(tmp, "w") as f:
        json.dump(payload, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, dst)
    return dst
