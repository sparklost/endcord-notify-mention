import logging
import re

from endcord import peripherals

EXT_NAME = "Notify Mention"
EXT_VERSION = "0.1.0"
EXT_ENDCORD_VERSION = "1.3.0"
EXT_DESCRIPTION = "An extension that sends desktop notification when specific regexes or words are matched in message in specific channels or guilds"
EXT_SOURCE = "https://github.com/sparklost/endcord-notify-mention"
logger = logging.getLogger(__name__)


class Extension:
    """Main extension class"""

    def __init__(self, app):
        self.app = app
        patterns = app.config.get("ext_notify_mention_match_regexes", [])
        contains = app.config.get("ext_notify_mention_match_contains", [])
        self.listen_channel = app.config.get("ext_notify_mention_listen_channel", [])
        self.listen_guilds = app.config.get("ext_notify_mention_listen_guilds", [])
        self.patterns = []
        for regex in patterns:
            try:
                self.patterns.append(re.compile(regex, re.IGNORECASE))
            except Exception:
                continue
        self.contains = []
        for word in contains:
            if isinstance(word, list):
                self.contains.append([x.lower() for x in word])
            else:
                self.contains.append(word.lower())

    def on_message_event(self, new_message):
        """Ran when message event is received"""
        data = new_message["d"]
        if data["channel_id"] not in self.listen_channel and data["guild_id"] not in self.listen_guilds:
            return

        if new_message["op"] == "MESSAGE_CREATE" and data["user_id"] != self.app.my_id and data["user_id"] not in self.app.blocked:
            if self.patterns:
                text = data["content"]
                for expression in self.patterns:
                    match = re.search(expression, text)
                    if match:
                        break
                else:
                    return
            elif self.contains:
                text = data["content"].lower()
                for expression in self.contains:
                    if isinstance(expression, list):
                        if all(sub in text for sub in expression):
                            match = str(expression)
                            break
                    elif expression in text:
                        match = expression
                        break
                else:
                    match = None
            else:
                match = None

            if match:
                title = f'Mention of "{match}" detected!'
                body = ""
                if data["guild_id"]:
                    guild_id = data["guild_id"]
                    channel_id = data["channel_id"]
                    for guild in self.app.guilds:
                        if guild["guild_id"] == guild_id:
                            body += f"[{guild["name"]}] "
                            break
                    for channel in guild["channels"]:
                        if channel["id"] == channel_id and channel.get("permitted"):
                            body += f"#{channel["name"]} - "
                            break
                body += f"{data["global_name"] if data["global_name"] else data.get("username")} said: {data["content"]}"
                logger.info(f"{title}\n  {body}")
                peripherals.notify_send(
                    title,
                    body,
                    sound=self.app.notification_sound,
                    custom_sound=self.app.notification_path,
                )
