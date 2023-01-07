__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
leader.py
- Leader election utilities
"""

from flask import current_app
from threading import Thread
import time
import os
from statesman_discord import constants
from leaderelection import Elect


class LeaderElection(object):
    def __init__(self, callback, *args, **kwargs):
        super(object, self).__init__(*args, **kwargs)

        if os.environ.get('POD') is None:
            current_app.logger.warn("Not running in a k8s cluster; not setting up leader election")
            self.election = None
            return

        self.election = Elect(configmap=os.environ.get(constants.LEADER_CONFIGMAP_NAME, f'{os.environ['NAMESPACE']}-leader'))

        self.callback = callback

        self.election_thread = Thread(target=self.election.run)
        self.election_thread.setDaemon(True)
        self.election_thread.start()

        self.watcher_thread = Thread(target=self._watcher)
        self.watcher_thread.setDaemon(True)
        self.watcher_thread.start()

    def _watcher(self):
        while True:
            current_app.logger.debug("checking leader status...")
            if am_i_leader():
                current_app.logger.info("I am the leader.")
                self.callback()
            time.sleep(int(os.environ.get(constants.LEADER_WATCHER_SLEEP, 1)))

    def am_i_leader(self):
        if self.election is None:
            current_app.logger.debug("Leader election not setup.")
            return False

        return self.election.check_leader()
