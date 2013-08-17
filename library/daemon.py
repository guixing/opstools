
import time
import os
import sys

def run():
    while True:
        print '1time'
        time.sleep(1)

def daemon():
    try:
        pid = os.fork()
        if pid > 0:
           sys.exit(0)
    except OSError, e:
        print 'fork #1 fail', e
        sys.exit(1)
    os.chdir('/')
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
           print 'daemon pid %d' % pid
           sys.exit(0)
    except OSError, e:
        print 'fork #2 fail', e
        sys.exit(1)
    nulldev = '/dev/null'
    stdin = file(nulldev, 'r')
    stdout = file('/tmp/stdout', 'a+', 0)
    stderr = file(nulldev, 'a+', 0)
    os.dup2(stdin.fileno(), sys.stdin.fileno())
    os.dup2(stdout.fileno(), sys.stdout.fileno())
    os.dup2(stderr.fileno(), sys.stderr.fileno())
    return pid

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-d':
        daemon()
    run()
