__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
setup.py
- Discord setup
"""

import os, json, logging
from statesman_discord import constants
from statesman_discord.utils.discord.commands import register_command
from kubernetes import client


def register_commands():
    logging.debug("")

    with open(os.environ[constants.DISCORD_COMMANDS_FILE_PATH], "r") as f:
        command_data = json.load(f)

        k8v1 = client.CoreV1Api()
        try:
            cm = k8v1.read_namespaced_config_map(name=os.environ[constants.LEADER_CONFIGMAP_NAME], namespace=os.environ[constants.NAMESPACE])
            logging.debug("cm: %s", cm)
        except Exception as e:
            logging.warn("Unable to read configmap {%s/%s}: %s", os.environ[constants.NAMESPACE], os.environ[constants.LEADER_CONFIGMAP_NAME], e)
            return

        cm_data = cm.to_dict()["data"] or {}
        logging.debug("cm_data: %s", cm_data)
        cm_version = int(cm_data.get(constants.LEADER_CONFIGMAP_KEY_COMMANDS_VERSION, "0"))
        logging.info("cm_version=%d", cm_version)

        # check last version of commands
        file_version = int(command_data.get("version", "0"))
        logging.info("file_version=%d", file_version)

        if file_version <= cm_version:
            logging.info("Commands file version is not newer; skipping commands registration.")
            return

        commands = command_data.get("commands", [])
        logging.info("Registering %d commands", len(commands))
        for command in commands:
            logging.info("Registering command: %s", command)
            register_command(command, os.environ[constants.DISCORD_TOKEN])

        # record command version in configmap
        logging.info("Updating leader configmap with latest version of commands: %d", file_version)
        cm_data[constants.LEADER_CONFIGMAP_KEY_COMMANDS_VERSION] = f"{file_version}"
        new_cm = client.V1ConfigMap(metadata=cm.to_dict()["metadata"], data=cm_data)
        logging.debug("new_cm: %s", new_cm)
        try:
            resp = k8v1.replace_namespaced_config_map(os.environ[constants.LEADER_CONFIGMAP_NAME], os.environ[constants.NAMESPACE], new_cm)
            logging.info("resp: %s", resp)
        except Exception as e:
            logging.warn("Unable to write configmap {%s/%s}: %s", os.environ[constants.NAMESPACE], os.environ[constants.LEADER_CONFIGMAP_NAME], e)
