import time

import flask

from .visitor import Visitor

class VisitorCollection(object):
    """
    A collection of Visitors which works with flask.session
    """

    def __init__(self, timeout=60):
        """
        Initialize the collection of Visitors

        timeout: seconds to keep an inactive Visitor in the collection
        """
        self.timeout = timeout
        self._visitors = {}

    def add(self, visitor):
        flask.session['visitorid'] = visitor.id
        self._visitors[visitor.id] = visitor
        return visitor

    def all(self, asjson=False):
        """
        Return a list of all visitors in the collection
        """
        if asjson:
            return [x.__json__() for x in self._visitors.values()]
        return self._visitors.values()

    def get(self, visitorid):
        return self._visitors.get(visitorid)

    # This works better than Flask-Login's meager support for anonymous users.
    def get_me(self):
        visitorid = None
        if 'visitorid' in flask.session:
            visitorid = flask.session['visitorid']
        return self.get(visitorid) or self.add(Visitor())

    def prune(self):
        """
        Remove visitors which visited after the expiration
        """
        expiration = int(time.time()) - self.timeout
        items = self._visitors.items()
        self._visitors = dict((k, v)
                for k, v in items
                if v.is_recent(expiration))
