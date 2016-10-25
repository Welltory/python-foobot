# -*- coding: utf-8 -*-

__all__ = [
    'FoobotBaseError',
    'FoobotOAuthError',
    'FoobotAPIError',
    'FoobotRefreshTokenError',
]


class FoobotBaseError(Exception):
    def __str__(self):
        return "*** %s (%s) *** : %s" % (self.status, self.reason, self.msg)


class FoobotOAuthError(FoobotBaseError):
    def __init__(self, status, reason, msg={}):
        self.status = status
        self.reason = reason
        self.msg = {}


class FoobotAPIError(FoobotBaseError):
    def __init__(self, resp):
        self.status = resp.status_code
        self.reason = resp.reason
        self.msg = resp.text


class FoobotRefreshTokenError(FoobotBaseError):
    pass
