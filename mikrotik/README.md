# MikroTik

Scripts for interaction with MikroTik routers

## Prerequisites

DSA key pair needed for this. You also need to import the public key for your router user.

```
$ ssh-keygen -t dsa -b 1024
```

## Backup 

*mikrotik_backup.sh* - make backup configuration of Mikrotik router and upload it on git repository

### Settings

```bash
BASEDIR="/backups/routers"
IDENT='~/.ssh/id_dsa'
OPTIONS="-oPubkeyAcceptedKeyTypes=+ssh-dss"
ROUTERS="router01 router02"
USER="admin"
```

```
