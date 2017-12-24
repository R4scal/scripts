#!/bin/bash
#title           :mikrotik_backup.sh
#description     :This script will make backup configuration of Mikrotik router
#                 and upload it on git repository
#author		 :rascal
#date            :20171222
#version         :0.2    
#usage		 :bash mikrotik_backup.sh
#==============================================================================

TODAY=$(/bin/date +%Y-%m-%d)
HOUR=$(/bin/date +%H-00)
COMPACT=$(/bin/date +%Y%m%d_%H%M)
PWD=`pwd`

BASEDIR="/backups/routers"
IDENT='~/.ssh/id_dsa'
OPTIONS="-oPubkeyAcceptedKeyTypes=+ssh-dss"
ROUTERS="router01 router02"
USER="admin"

if [ "$1" == "debug" ]; then
  set -x
fi

# Backup
for ROUTER in $ROUTERS; do
/usr/bin/ssh $OPTIONS -i $IDENT $USER@$ROUTER "/export file=export_${COMPACT}" && \
    /usr/bin/scp $OPTIONS -i $IDENT -q $USER@$ROUTER:/export_${COMPACT}.rsc $BASEDIR/${ROUTER}.rsc && \
    /usr/bin/ssh $OPTIONS -i $IDENT $USER@$ROUTER "/file remove export_${COMPACT}.rsc"

/usr/bin/ssh $OPTIONS -i $IDENT $USER@$ROUTER "/system backup save name=backup_${COMPACT}" &>/dev/null && \
    sleep 1 && \
    /usr/bin/scp $OPTIONS -i $IDENT -q $USER@$ROUTER:/backup_${COMPACT}.backup $BASEDIR/${ROUTER}.backup && \
    /usr/bin/ssh $OPTIONS -i $IDENT $USER@$ROUTER "/file remove backup_${COMPACT}.backup"
done

# Upload backup to git
cd $BASEDIR
/usr/bin/git add --all
/usr/bin/git commit -m "Backup on ${TODAY}"
/usr/bin/git push

# Return to working dir
cd $PWD
