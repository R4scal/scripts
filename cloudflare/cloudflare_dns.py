#!/bin/python

import getopt
import sys
import CloudFlare

def main():
    zone_name = 'example.com'
    email = 'admin@example.com'
    token = '<secret token>'

    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:i", ["dns=", "ip=", "add", "delete"])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)
    dns_name = ''
    ip_address = ''
    action = ''
    for o, a in opts:
       if o == "--add":
          action = 'add'
       elif o == "--delete":
          action = 'delete'
       elif o == "--dns":
          dns_name = a
       elif o == "--ip":
          ip_address = a
       else:
            assert False, "unhandled option"

    if ip_address == '':
        exit('ip empty')
    if dns_name == '':
        exit('dns empty')

    cf = CloudFlare.CloudFlare(email=email,token=token)

    # query for the zone name and expect only one value back
    try:
        zones = cf.zones.get(params = {'name':zone_name,'per_page':1})
    except Exception as e:
        exit('/zones.get - %s - api call failed' % (e))

    # extract the zone_id which is needed to process that zone
    zone = zones[0]
    zone_id = zone['id']


    if action == 'add':
       add_record(cf, zone_id, dns_name, ip_address)
    elif action == 'delete':
       delete_record(cf, zone_id, dns_name, ip_address)

    exit(0)

def add_record(cf, zone_id, dns_name, ip_address):
    dns_data = {
      'name':dns_name,
      'type':'A',
      'content':ip_address,
      'proxied':True,
    }
    try:
       res = cf.zones.dns_records.post(zone_id, data=dns_data)
    except Exception as e:
       exit('/zones.post - %s - api call failed' % (e))
    print 'CREATED: %s %s' % (dns_name, ip_address)
    exit(0)

def delete_record(cf, zone_id, dns_name, ip_address):
    rec_id = ''
    # request the DNS records from that zone
    try:
        dns_records = cf.zones.dns_records.get(zone_id)
    except Exception as e:
        exit('/zones/dns_records.get %d %s - api call failed' % (e, e))

    # then all the DNS records for that zone
    for dns_record in dns_records:
        if dns_record['type'] not in ['A', 'AAAA']:
            # we only deal with A / AAAA records
            continue
        if dns_record['name'] == dns_name and dns_record['content'] == ip_address:
            rec_id = dns_record['id']
        else:
            continue
    if rec_id != '':
        dns_data = {
           'name':dns_name,
           'type':'A',
           'content':ip_address,
        }
        try:
            res = cf.zones.dns_records.delete(zone_id, rec_id, data=dns_data)
        except Exception as e:
            exit('/zones.delete - %s - api call failed' % (e))
        print 'DELETED: %s %s' % (dns_name, ip_address)
    exit(0)

if __name__ == '__main__':
    main()
