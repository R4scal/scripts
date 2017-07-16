# Сloudflare

Scripts for interaction with API Сloudflare

## Prerequisites

*cloudflare-python* package is needed.

```
$ sudo pip install cloudflare
```

## DNS

*cloudflare_dns.py* - manage DNS records

### Settings

```python
zone_name = 'example.com'
email = 'admin@example.com'
token = '<secret token>'
```

### Create DNS record

```
./cloudflare_dns.py --dns example.com --ip 1.1.1.1 --add
```

### Delete DNS record

```
./cloudflare_dns.py --dns example.com --ip 1.1.1.1 --delete
```
