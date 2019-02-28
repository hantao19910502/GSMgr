#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys,os


#命令
rename_exists = "ls /home/pirate/programs/mysql/bin | grep -w mysql_rename_db | wc -l"
rename_cmd = "cd /home/pirate/programs/mysql/bin && sh mysql_rename_db -u%s -p%s -f %s -t pirate%s"
args_exists = "ls %s | grep game%s.args | wc -l"
gsc_exists = "ls %s | grep game%s | wc -l"
dataproxy_exists = "ls %s | grep pirate%s | wc -l"
dataproxy_cmd = "cd %s && sh init.sh pirate%s"
init_exists = "ls %s | grep init.sh | wc -l"
init_cmd = "cd %s && source ~/.bash_profile && sh init.sh game%s"
check_start_cmd = "sh %s/utils/check_start.sh %s game%s %s"
check_init_cmd = "cd %s && source ~/.bash_profile && sh init.sh game%s check"
