# endcord-notify-mention
An extension for [endcord](https://github.com/sparklost/endcord) discord TUI client, that sends desktop notification when specific regexes or words are matched in message in specific channels or guilds.  
Matched messages are also added to the log.

## Installing
See [official extensions documentation](https://github.com/sparklost/endcord/blob/main/extensions.md#installing-extensions) for installing instructions.
- Git clone into `Extensions` directory located in endcord config directory.
- run `endcord -i https://github.com/sparklost/endcord-notify-mention` (must have `git` installed)


## Configuration
All extension options are under `[main]` section in endcord config. This extension options are always prepended with `ext_notify_mention_`.

### Settings options
- `ext_notify_mention_match_regexes = []`  
    List of regex strings used to match messages.
- `ext_notify_mention_match_contains = []`  
    List of strings, if any is inside the message, will trigger a match. Can also be list of lists of strings, where all strings must be inside a message to trigger a match (eg `["test", ["hello", "world"]]` will match any message containing "test" or both "hello" and "world"). Strings are case insensitive.
- `ext_notify_mention_listen_channel = []`  
    List of channel IDs where to monitor messages. IDs must be strings (`"12345"`).
- `ext_notify_mention_listen_guilds = []`  
    List of server IDs where to monitor messages. IDs must be strings (`"12345"`). Overrides `ext_notify_mention_listen_channel` if channels are from same server.


## Disclaimer
> [!WARNING]
> Using third-party client is against Discord's Terms of Service and may cause your account to be banned!  
> **Use endcord and/or this extension at your own risk!**
> If this extension is modified, it may be used for harmful or unintended purposes.
> **The developer is not responsible for any misuse or for actions taken by users.**
