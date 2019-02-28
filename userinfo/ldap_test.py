#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
   * File Name : ldap_test.py

   * Purpose :

   * Creation Date : 01-04-2016

   * Last Modified :

   * Created By : dren
'''
import sys
from ldap3 import Server, Connection, SYNC, AUTH_SIMPLE, NTLM


class ActiveDirectoryBackend:

    def authenticate(self, username=None, password=None):

        if len(password) == 0:
            return None
        s = Server('ldap://192.168.2.40', get_info=None)  # define an unsecure LDAP server, requesting info on DSE and schema
        c = Connection(s,
                       auto_bind=True,
                       client_strategy=SYNC,
                       user="uid={0},ou=Users,dc=babeltime,dc=com".format(username),
                       password=password,
                       authentication=AUTH_SIMPLE,
                       )
        print
        c.unbind()
        return r


if __name__ == '__main__':
    l = ActiveDirectoryBackend()
    print l.authenticate('liudechuan', 'JQdp5f6-a5')
