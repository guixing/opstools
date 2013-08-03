#!/usr/bin/env python2.7
#
#
import sys
from os import path
import os
DIRNAME = path.dirname(__file__)
OPSTOOLS_DIR = path.abspath(path.join(DIRNAME, '..'))
sys.path.append(OPSTOOLS_DIR)

from library.mysql import MySQLDConfig
from optparse import OptionParser

MYSQL_DATA_DIR = "/var/mysqlmanager/data"
MYSQL_CONF_DIR = "/var/mysqlmanager/cnfs"


def opts():
    parser = OptionParser(usage="usage: %prog options")
    parser.add_option("-c", "--cmd", 
                      dest="cmd", 
                      action="store",
                      default="check",)
    parser.add_option("-n", "--name", 
                      dest="name", 
                      action="store",
                      default="mysqlinstance",)
    parser.add_option("-p", "--port", 
                      dest="port", 
                      action="store",
                      default="3306",)
    return parser.parse_args()


def readConfs():
    import glob
    confs = glob.glob(path.join(MYSQL_CONF_DIR,'*.cnf'))
    return [MySQLDConfig(c) for c in confs]

def checkPort(d, p):
    for m in d:
        if p == m.mysqld_vars['port']:
            return True
    return False

def _genDict(name, port):
    return {
        "pid-file": path.join(MYSQL_DATA_DIR, name,"%s.pid" % name ),
        "socket": "/tmp/%s.sock" % name,
        "port": port,
        "datadir": path.join(MYSQL_DATA_DIR, name),
        "log_error": path.join(MYSQL_DATA_DIR,"%s.log" % name),
    }

def mysql_install_db(cnf):
    from subprocess import Popen, PIPE
    p = Popen("mysql_install_db --defaults-file=%s"%cnf, shell=True)
    stdout, stderr = p.communicate()
    return p.returncode

def setOwner(p, user):
    os.system("chown -R mysql:mysql %s" % p) 

def createInstance(name, port):
    cnf = path.join(MYSQL_CONF_DIR, "%s.cnf" % name)
    datadir = path.join(MYSQL_DATA_DIR, name)
    exists_cnfs = readConfs()
    if checkPort(exists_cnfs, port):
        print >> sys.stderr, "Port exist"
        sys.exit(-1)
    if not path.exists(cnf):
        c = _genDict(name, port)
        mc = MySQLDConfig(cnf, **c)
        mc.save()
    else:
        mc = MySQLDConfig(cnf)
    if not path.exists(datadir):
        mysql_install_db(cnf)
        setOwner(datadir, mc.mysqld_vars['user'])

def _init():
    if not path.exists(MYSQL_DATA_DIR):
        os.makedirs(MYSQL_DATA_DIR)
    if not path.exists(MYSQL_CONF_DIR):
        os.makedirs(MYSQL_CONF_DIR)

def main():
    _init()
    opt, args = opts()
    instance_name = opt.name
    instance_port = opt.port
    command = opt.cmd
    if command == "create":
        createInstance(instance_name, instance_port)

if __name__ == '__main__':
    main()
