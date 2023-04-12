import subprocess, sys, os, tempfile, shutil
from ctypes import *

CLONE_NEWPID = 0x20000000

def main():
    command = sys.argv[3]
    args = sys.argv[4:]

    libc = CDLL("libc.so.6")
    jdirs = ["usr/bin", "usr/local/bin", "lib/x86_64-linux-gnu", "lib64"]
    pid_ns = libc.unshare(CLONE_NEWPID)

    with tempfile.TemporaryDirectory() as jail:
        os.chdir(jail)
        for j_dir in jdirs:
            os.makedirs(j_dir)
        shutil.copy("/usr/local/bin/docker-explorer", "usr/local/bin/")
        os.chroot(".")

        completed_process = subprocess.run([command, *args], capture_output=True)
        sys.stdout.write(completed_process.stdout.decode("utf-8"))
        sys.stderr.write(completed_process.stderr.decode("utf-8"))
    
    sys.exit(completed_process.returncode)


if __name__ == "__main__":
    main()
