#!/usr/bin/env python

import urllib, urllib2
import json
import os 
CURR_DIR=os.path.abspath(os.path.dirname(__file__))
HOST_CONF_DIR=os.path.join(CURR_DIR,'hosts')
CACHE_FILE='/var/tmp/api-cache.json'

HOST_TMP="""define host {
        use                     linux-server
        host_name              	%(hostname)s
        alias                   %(hostname)s
        address                 %(ipaddr)s
    	contact_groups		admins
}
"""

def getHosts():
    url = "http://localhost:8000/api/gethosts.json"
    try:
        data = urllib2.urlopen(url).read()
        writeFile(CACHE_FILE, data)
    except:
        data = open(CACHE_FILE,'r').read()
    return json.loads(data)

def initDir():
    if not os.path.exists(HOST_CONF_DIR):
        os.mkdir(HOST_CONF_DIR)

def writeFile(f,s):
    with open(f,'w') as fd:
        fd.write(s)

def genNagiosHost(hostdata):
    initDir()
    conf = os.path.join(HOST_CONF_DIR,'hosts.cfg')
    hostconf = ""
    for hg in hostdata:
        for h in hg['members']:
            hostconf += HOST_TMP % h
    writeFile(conf,hostconf)

def main():
    result = getHosts()
    if result['status'] == 0:
        print genNagiosHost(result['data'])
    else:
        print 'Err: %s' % result['message']

if __name__=="__main__":
    main()
