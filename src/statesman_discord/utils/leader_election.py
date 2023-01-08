__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
leader.py
- Leader election utilities
"""

from threading import Thread
import os
from statesman_discord import constants
from statesman_discord.utils.discord.setup import register_commands
from kubernetes import config
from kubernetes.leaderelection import leaderelection
from kubernetes.leaderelection.resourcelock.configmaplock import ConfigMapLock
from kubernetes.leaderelection import electionconfig


class LeaderElection(object):
    def __init__(self, app) -> None:
        self.is_leader = False
        self.app = app

        if os.environ.get(constants.POD) is None:
            return

        self.logger = app.logger

        self.logger.info("Loading cluster config...")
        config.load_incluster_config()
        self.candidate_id = os.environ[constants.POD]
        self.lock_name = os.environ.get(constants.LEADER_CONFIGMAP_NAME, f"{os.environ[constants.NAMESPACE]}-leader")
        self.lock_namespace = os.environ[constants.NAMESPACE]

        self.logger.debug("Creating election config...")
        self.election_config = electionconfig.Config(
            ConfigMapLock(self.lock_name, self.lock_namespace, self.candidate_id),
            lease_duration=17,
            renew_deadline=15,
            retry_period=5,
            onstarted_leading=self._leader_callback,
            onstopped_leading=self._follower_callback,
        )

        # Enter leader election
        self.elect = leaderelection.LeaderElection(self.election_config)

        self.logger.info("Starting election thread...")
        # self.elect.run()
        app.executor.submit(self.elect.run)
        # self.election_thread = Thread(target=self.elect.run)
        # self.election_thread.setDaemon(True)
        # self.election_thread.start()

    def _leader_callback(self):
        self.logger.info("I am the leader; executing setup...")

        self.is_leader = True

        register_commands()

    def _follower_callback(self):
        self.logger.info("I am not the leader.")

        self.is_leader = False
