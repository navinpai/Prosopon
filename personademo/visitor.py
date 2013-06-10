import time
import uuid

import flask

class Visitor(object):
    """
    A visitor to the web site
    """

    def __init__(self, identifier=None):
        self.identifier = identifier is not None and identifier or 'Anonymous'
        self.id = str(uuid.uuid1())
        self.refresh()

    def __json__(self):
        return dict(
                id=self.id,
                identifier=self.identifier,
                lastpath=self.lastpath,
                lastvisit=self.lastvisit,
        )

    def deidentify(self):
        self.identifier = 'Anonymous'

    def get_id(self):
        return self.id

    def identify(self, identifier=None):
        if identifier is None:
            if 'Anonymous' == self.identifier:
                return ''
        else:
            self.identifier = identifier
        return self.identifier

    def is_active(self, expirationtime):
        return True

    def is_anonymous(self):
        return 'Anonymous' == self.identifier

    def is_authenticated(self):
        return 'Anonymous' != self.identifier

    def is_recent(self, expirationtime):
        return self.lastvisit > expirationtime

    def this_is_you(self):
        if self.id == flask.session['visitorid']:
            return '(This is you)'
        return ''

    def refresh(self):
        self.lastvisit = int(time.time())
        self.lastpath = flask.request.path
