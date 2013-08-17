#!/usr/bin/env python


import dns.update
import dns.tsigkeyring

key = "mQx7YHOWLzEDXy2HXwhAvM70wC1ks330ZQontYAXV5qv3TZxTH2QZBzOxJ/WtWpPgH7mkpRtABb7UNLg5+HpWw=="

keyring = dns.tsigkeyring.from_text({
    'example.net':key
})

rr = [
    '192.168.1.135',
    '192.168.1.136',
]

up = dns.update.Update('example.net',keyring=keyring)
ttl = 60

rdata_list = [dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.A,i) for i in rr]
rdata_set = dns.rdataset.from_rdata_list(ttl,rdata_list)

up.replace('www', rdata_set)

import dns.query
q = dns.query.tcp(up, '127.0.0.1')

print q



