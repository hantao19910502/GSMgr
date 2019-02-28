#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
from backend.lib.exception import SSHParamError


class SSHConn:
    def __init__(self, host, user, passwd=None, mode='rsa', pkey=None):
        self.host=host
        self.user=user
        self.passwd=passwd
        self.mode=mode
        self.pkey=pkey
	
        self.pkey_modes = {'rsa': paramiko.RSAKey, 'dsa': paramiko.DSSKey}

    def scp_conn(self):

        self.conn = paramiko.Transport((self.host, 22))
        if self.passwd:
            self.conn.connect(username=self.user, password=self.passwd) 
        else:
            self.conn.connect(username=self.user, pkey=self.pkey_modes[self.mode].from_private_key_file(self.pkey))

        self.sftp = paramiko.SFTPClient.from_transport(self.conn)

    def cmd_conn(self):

        self.conn = paramiko.SSHClient()
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.passwd:
            self.conn.connect(self.host, 22, self.user, self.passwd) 
        else:
            self.conn.connect(hostname=self.host, port=22, username=self.user, pkey=self.pkey_modes[self.mode].from_private_key_file(self.pkey))

    def __del__(self):
        self.conn.close()
    
    def cmd(self, cmd):

        self.cmd_conn()

        stdin, stdout, stderr = self.conn.exec_command(cmd)
        outtext = stdout.read()
        errtext = stderr.read()

        channel = stdout.channel
        status = channel.recv_exit_status()

        if status != 0:
            return False, str(outtext) + str(errtext)

        return True, outtext

    def put(self, localfile, remotefile):

        self.scp_conn()
        self.sftp.put(localfile, remotefile)

    def get(self, remotepath, localpath):

        self.scp_conn()
        self.sftp.get(remotepath, localpath)

def get_default_private_key():
    
    pkeys = {'rsa': str(os.environ['HOME']) + '/.ssh/id_rsa', 'dsa': str(os.environ['HOME']) + '/.ssh/id_dsa'}

    mode=""
    pkey=""

    for k,v in pkeys.items():

       if os.path.isfile(v):
           mode=k
           pkey=v

           break
    return mode,pkey


def scp(host, fromfile, tofile, user=None, passwd=None, method='put', mode=None, pkey=None):

    if not pkey and not mode:
        mode,pkey = get_default_private_key()

    elif not (pkey and mode):
        raise SSHParamError("you should specify private key mode when you had specified a private key")

    if not user:
        user=str(os.environ['USER'])

    ss = SSHConn(host, user, passwd, mode, pkey)

    if method == "put":
        ss.put(fromfile, tofile)

    elif method == "get":
        ss.get(fromfile, tofile)

def cmd(host, cmd, user=None, passwd=None, mode=None, pkey=None):

    if not pkey and not mode:
        mode,pkey = get_default_private_key()

    elif not (pkey and mode):
        raise SSHParamError("you should specify private key mode when you had specified a private key")


    if not user:
        user=str(os.environ['USER'])

    sc = SSHConn(host, user, passwd, mode, pkey)

    return sc.cmd(cmd)
