__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
leader.py
- Leader election utilities
"""

from flask import current_app
import logging
from threading import Thread
import time
import os
from statesman_discord import constants
from leaderelection import Elect
from statesman_discord.utils.discord.setup import register_commands


class LeaderElection(object):
    def __init__(self, callback, *args, **kwargs):
        super(object, self).__init__(*args, **kwargs)

        if os.environ.get(constants.POD) is None:
            logging.warn("Not running in a k8s cluster; not setting up leader election")
            self.election = None
            return

        self.election = Elect(configmap=os.environ.get(constants.LEADER_CONFIGMAP_NAME, f"{os.environ[constants.NAMESPACE]}-leader"))
        self.is_leader = False

        self.callback = callback

        self.election_thread = Thread(target=self.election.run)
        self.election_thread.setDaemon(True)
        self.election_thread.start()

        self.watcher_thread = Thread(target=self._watcher)
        self.watcher_thread.setDaemon(True)
        self.watcher_thread.start()

    def am_i_leader(self):
        if self.election is None:
            logging.debug("Leader election not setup.")
            return True

        return self.election.check_leader()

    def _watcher(self):
        while True:
            logging.debug("Checking leader status...")
            is_leader = self.am_i_leader()
            logging.debug("Am I the leader? %s (was: %s)", is_leader, self.is_leader)
            if is_leader != self.is_leader:
                logging.info(f"Leader state changed from {self.is_leader} to {is_leader}.")
                self.is_leader = is_leader
                self.callback(is_leader)

            sleep_time = int(os.environ.get(constants.LEADER_WATCHER_SLEEP, 1))
            logging.debug("Sleeping for %d seconds...", sleep_time)
            time.sleep(sleep_time)


def leader_callback(is_leader: bool):
    current_app.logger.debug("is_leader: %s", is_leader)

    if is_leader:
        current_app.logger.info("I am the leader; executing setup...")
        register_commands()
