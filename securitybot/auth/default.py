'''
Default Authentication.
'''
__author__ = 'Yanlin Wang'
__email__ = 'yanlin.wang@centrify.com'

import logging
from datetime import datetime
from urllib import urlencode
from securitybot.auth.auth import Auth, AUTH_STATES, AUTH_TIME

from typing import Any

class DefaultAuth(Auth):
    def __init__(self, username):
        # type: (Any, str) -> None
        '''
        Args:
            duo_api (duo_client.Auth): An Auth API client from Duo.
            username (str): The username of the person authorized through
                            this object.
        '''
        self.username = username
        self.txid = None # type: str
        self.auth_time = datetime.min
        self.state = AUTH_STATES.NONE

    def can_auth(self):
        # type: () -> bool
        # Use Duo preauth to look for a device with Push
        # TODO: This won't work for anyone who's set to auto-allow, but
        # I don't believe we have anyone like that...
        logging.debug('Checking auth capabilities for {}'.format(self.username))

        return True

    def auth(self, reason=None):
        # type: (str) -> None
        pushinfo = 'from=Securitybot'
        if reason:
            pushinfo += '&'
            pushinfo += urlencode({'reason': reason})

        self.txid = 'txid'
        self.state = AUTH_STATES.AUTHORIZED

    def _recently_authed(self):
        # type: () -> bool
        return (datetime.now() - self.auth_time) < AUTH_TIME

    def auth_status(self):
        # type: () -> int
        return AUTH_STATES.AUTHORIZED

    def reset(self):
        # type: () -> None
        self.txid = None
        self.state = AUTH_STATES.NONE
