# -*- coding: utf-8 -*-


class BaseError(Exception):
    """ Base queue job error """

class SSHParamError(BaseError):
    """ A ssh init param has an error """

class SSHConnError(BaseError):
    """ A ssh conn has an error """
