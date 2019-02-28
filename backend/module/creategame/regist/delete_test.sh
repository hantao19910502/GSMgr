#!/bin/bash


serverid="10023"
mainhost="192.168.1.140"
mdbhost="192.168.1.140"
sdbhost="192.168.1.145"
logichost="192.168.1.145 192.168.2.23"
tmpname=`date +'%m%d%H%M%S'`


cd /home/pirate/django/GSMgr/backend/module/creategame/tmp/lcserver && rm -rf game${serverid}.args
cd /home/pirate/django/GSMgr/backend/module/creategame/tmp/rpcfw && rm -rf game${serverid}

ssh $mdbhost "~/programs/mysql/bin/mysql -uroot -p2WTWzvor8qASHZfjII2FNdJKOSwDQ5Rm -e 'create database tmp$tmpname;'"
ssh $mdbhost "~/programs/mysql/bin/mysql -uroot -p2WTWzvor8qASHZfjII2FNdJKOSwDQ5Rm -e 'drop database pirate$serverid;'"

ssh $mainhost "cd /home/pirate/lcserver/conf && rm -rf game${serverid}.args;cd /home/pirate/rpcfw/conf/gsc && rm -rf game$serverid"

for i in $logichost;do
    ssh $i "cd /home/pirate/rpcfw/conf/gsc && rm -rf game$serverid"
done

ssh $sdbhost "cd /home/pirate/dataproxy/data && rm -rf pirate$serverid"
