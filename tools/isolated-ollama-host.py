#!/usr/bin/env python3
"""SSH-stdin helper: restrict Ollama writes to a temporary RAM directory.

The caller stores this source and all logs on its own machine. This helper is
never installed on the host. Existing model weights are used read-only.
"""
import argparse
import ctypes
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import subprocess
import tempfile
import threading
import sys


class Ruleset(ctypes.Structure):
    _fields_ = [('handled_access_fs', ctypes.c_uint64)]


class PathBeneath(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('allowed_access', ctypes.c_uint64), ('parent_fd', ctypes.c_int32)]


def restrict_writes(scratch):
    libc = ctypes.CDLL(None, use_errno=True)
    abi = libc.syscall(444, 0, 0, 1)
    if abi < 3:
        raise OSError('Landlock ABI >=3 is required, including truncate restrictions')
    # Reads and execution remain available; writes, deletion, creation, renaming
    # and truncation are denied unless explicitly allowed under this RAM path.
    write = sum(1 << bit for bit in range(4, 15)) | (1 << 1)
    attr = Ruleset(write)
    ruleset = libc.syscall(444, ctypes.byref(attr), ctypes.sizeof(attr), 0)
    if ruleset < 0:
        raise OSError(ctypes.get_errno(), 'landlock_create_ruleset')
    try:
        device_rules = [(str(path), 1 << 1) for path in Path('/dev').glob('nvidia*') if path.is_char_device()]
        # CUDA names its threads through procfs. Runner subprocesses have a
        # different /proc/self/task from the server; permit virtual process
        # metadata, with ordinary OS ownership and no-new-privileges retained.
        virtual_rules = [('/proc', (1 << 1) | (1 << 14))]
        for path, flags in [(scratch, write), ('/dev/null', (1 << 1) | (1 << 14)), *device_rules, *virtual_rules]:
            descriptor = os.open(path, os.O_PATH | os.O_CLOEXEC)
            try:
                rule = PathBeneath(flags, descriptor)
                if libc.syscall(445, ruleset, 1, ctypes.byref(rule), 0) < 0:
                    raise OSError(ctypes.get_errno(), 'landlock_add_rule')
            finally:
                os.close(descriptor)
        if libc.prctl(38, 1, 0, 0, 0) != 0:
            raise OSError(ctypes.get_errno(), 'PR_SET_NO_NEW_PRIVS')
        if libc.syscall(446, ruleset, 0) < 0:
            raise OSError(ctypes.get_errno(), 'landlock_restrict_self')
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    finally:
        os.close(ruleset)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--models', required=True)
    parser.add_argument('--port', type=int, default=11501)
    parser.add_argument('--probe', action='store_true')
    parser.add_argument('--heartbeats', action='store_true')
    args = parser.parse_args()
    scratch = Path(tempfile.mkdtemp(prefix='local-reader-', dir='/dev/shm'))
    child = None
    try:
        if args.probe:
            pid = os.fork()
            if pid == 0:
                try:
                    restrict_writes(str(scratch))
                    allowed = scratch / 'allowed'
                    allowed.write_text('ephemeral RAM probe')
                    denied = False
                    try:
                        with open('/tmp/local-reader-landlock-probe', 'wb'):
                            pass
                    except PermissionError:
                        denied = True
                    print(json.dumps({'host_disk_write_denied': denied, 'ram_write_allowed': allowed.exists(), 'ram_path': str(scratch)}), flush=True)
                    os._exit(0 if denied else 3)
                except Exception as error:
                    print(json.dumps({'probe_error': str(error)}), flush=True)
                    os._exit(2)
            _, status = os.waitpid(pid, 0)
            if os.waitstatus_to_exitcode(status):
                raise RuntimeError('Landlock probe failed')
            return
        env = dict(os.environ, HOME=str(scratch), TMPDIR=str(scratch),
                   XDG_CACHE_HOME=str(scratch / 'cache'), CUDA_CACHE_DISABLE='1',
                   OLLAMA_DEBUG='0', OLLAMA_NO_CLOUD='1', OLLAMA_HOST=f'127.0.0.1:{args.port}',
                   OLLAMA_MODELS=args.models, OLLAMA_NUM_PARALLEL='1',
                   OLLAMA_MAX_LOADED_MODELS='1', OLLAMA_KEEP_ALIVE='5m',
                   OLLAMA_FLASH_ATTENTION='1', OLLAMA_NOPRUNE='1', OLLAMA_NOHISTORY='1')
        def setup():
            ctypes.CDLL(None).prctl(1, signal.SIGTERM)
            restrict_writes(str(scratch))
        child = subprocess.Popen(['/usr/local/bin/ollama', 'serve'], env=env,
                                 cwd=scratch, preexec_fn=setup, start_new_session=True)
        def shutdown(signum, frame):
            raise SystemExit(0)
        for signum in [signal.SIGTERM, signal.SIGHUP, signal.SIGINT]:
            signal.signal(signum, shutdown)
        if args.heartbeats:
            def control_channel():
                for _ in sys.stdin:
                    pass
                os.kill(os.getpid(), signal.SIGTERM)
            threading.Thread(target=control_channel, daemon=True).start()
        child.wait()
    finally:
        if child and child.poll() is None:
            os.killpg(child.pid, signal.SIGTERM)
            try:
                child.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()
        if scratch.parent.resolve() != Path('/dev/shm') or not scratch.name.startswith('local-reader-'):
            raise RuntimeError('Unexpected cleanup target')
        shutil.rmtree(scratch)
        print(json.dumps({'ephemeral_ram_removed': str(scratch)}), flush=True)


if __name__ == '__main__':
    main()
