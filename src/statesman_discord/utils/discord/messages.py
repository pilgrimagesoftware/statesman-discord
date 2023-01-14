__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
messages.py
- Discord messaging functions
"""


from flask import current_app
import json, logging, os
import requests
from statesman_discord import constants
from statesman_discord.common.exceptions import SignatureException
from statesman_discord.utils.discord import _get_interaction_response_url


def send_message(response_url: str, data: list, private: bool):
    logging.debug("response_url: %s, data: %s, private: %s", response_url, data, private)

    body = json.dumps(
        {
            "private": private,
            "data": data,
        }
    )
    logging.debug("body: %s", body)
    r = requests.post(
        response_url,
        headers={
            "Content-type": "application/json",
        },
        data=body,
    )
    logging.debug("r: %s", r)


def handle_interaction_response(msg: dict):
    logging.debug("msg: %s", msg)

    answer = msg.get("answer")
    flags = 0
    if answer is None:
        content = "TBD"
    else:
        if answer.get("private"):
            flags |= constants.MSG_FLAG_EPHEMERAL

        contents = []
        for datum in answer.get("messages", []):
            if datum.get("text"):
                contents.append(datum["text"])
            elif datum.get("type"):
                thing = datum["type"]
                if thing == "divider":
                    contents.append("---")
            elif datum.get("items"):
                for item in datum["items"]:
                    if item.get("collection"):
                        collection = item["collection"]
                        name = collection["name"]
                        creator_info = collection.get("creator")
                        if creator_info:
                            creator = f"<@{creator_info.split('|',2)[-1]}>"
                        else:
                            creator = "no one"
                        contents.append(f"*{name}*\nCreated by {creator}")
                    elif item.get("item"):
                        state_item = item["item"]
                        name = state_item["name"]
                        label = state_item.get("label")
                        value = state_item["value"]
                        default = state_item.get("default")

                        if label:
                            content = f"*{label} ({name})* = {value}"
                        else:
                            content = f"*{name}* = {value}"
                        if default:
                            content += f" (default: {default})"
                        contents.append(content)

        content = "\n".join(contents)

    headers = {"Authorization": f"Bot {os.environ['DISCORD_TOKEN']}"}
    body = {
        "flags": flags,
        "content": content,
    }

    url = _get_interaction_response_url(msg["response_data"]["token"])
    r = requests.patch(url, headers=headers, json=body)
    logging.info("response: code=%d, headers=%s, body=%s", r.status_code, r.headers, r.json())
