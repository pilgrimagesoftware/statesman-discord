__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
commands.py
- Command parsing functions
"""


import logging


def construct_command(msg: dict) -> str:
    logging.debug("msg: %s", msg)

    cmd = msg["data"]["name"]
    logging.debug("cmd: %s", cmd)
    # TODO: check cmd

    parts = []
    for item in msg["data"]["options"]:
        name = item.get("name")
        if name:
            parts.append(name)

            for sub_item in item["options"]:
                option = sub_item.get("name")
                value = sub_item.get("value")

                parts.append(f"{option}={value}")
    # parts = list(map(lambda x: x["name"], msg["data"]["options"]))
    logging.debug("parts: %s", parts)
    # parts.append(list(map(lambda x: x["name"], msg["data"]["options"][0].get("options", []))))
    # logging.debug("more parts: %s", parts)
    command = " ".join(parts)
    logging.debug("command: %s", command)

    return command
